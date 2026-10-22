import asyncio
from pathlib import Path
from tempfile import TemporaryDirectory
from time import perf_counter
from uuid import UUID

from celery import Task
from celery.exceptions import Ignore, Reject, Retry
from langchain.chat_models import init_chat_model
from lecture_processor import OutputState
from lecture_processor.api import process_lecture
from lecture_processor.graph.context import ExtractionContext
from pydantic import BaseModel, Field, field_validator

from backend.core.logger import logger
from backend.courses.notes.models import NoteBlock
from backend.courses.notes.note_block_service import NoteBlockService
from backend.courses.notes.parser import parse_lecture_document
from backend.courses.vector_store.models import VectorStoreStatus
from backend.database.config import open_session
from backend.processing.celery_app import app
from backend.processing.resources import (
    block_builder,
    course_note_scope,
    course_vectorstore_scope,
    processing_update,
)

from .model import (
    LectureProcessingRun,
    ProcessingRun,
    ProcessingStage,
    ProcessingStatus,
)


class LectureProcessingInput(BaseModel):
    course_id: UUID
    note_id: UUID


class LecturingProcessingState(LectureProcessingInput):
    run_id: UUID
    file_id: UUID
    extraction_result: OutputState | None = None
    note_blocks: list[NoteBlock] = Field(default_factory=list)
    vector_ids: list[str] = Field(default_factory=list)

    @field_validator("note_blocks", mode="before")
    @classmethod
    def validate_note_blocks(cls, blocks):
        # SQLModel table constructors do not fully validate broker JSON.
        if isinstance(blocks, list):
            return [
                NoteBlock.model_validate(block) if isinstance(block, dict) else block
                for block in blocks
            ]
        return blocks


@app.task(bind=True, pydantic=True)
def process_lecture_file(self: Task, data: LectureProcessingInput):
    started = perf_counter()
    task_id = self.request.id
    logger.info(
        "Lecture processing started: task_id=%s course_id=%s note_id=%s",
        task_id,
        data.course_id,
        data.note_id,
    )
    try:
        chain = (
            prepare_lecture_run.s(data.model_dump(mode="json"))
            | extract_lecture_content.s()
            | parse_and_save_note_blocks.s()
            | embedd_and_save.s()
        )
        logger.debug(
            "Replacing task with preparation/extraction chain: task_id=%s", task_id
        )
        return self.replace(chain)
    except (Ignore, Retry, Reject):
        raise
    except Exception:
        logger.exception(
            "Lecture processing failed: task_id=%s course_id=%s "
            "note_id=%s elapsed_seconds=%.2f",
            task_id,
            data.course_id,
            data.note_id,
            perf_counter() - started,
        )
        raise


@app.task(bind=True, pydantic=True)
def prepare_lecture_run(self: Task, data: LectureProcessingInput) -> dict:
    run_id = None
    started = perf_counter()
    logger.info(
        "Preparation started: task_id=%s course_id=%s note_id=%s",
        self.request.id,
        data.course_id,
        data.note_id,
    )
    try:
        course_uuid = data.course_id
        note_uuid = data.note_id

        with course_note_scope() as course_notes:
            note = asyncio.run(course_notes.get_note_record(note_uuid))
            if note.course_id != course_uuid:
                raise ValueError("Note does not belong to the requested course")
            file = note.file
            if file is None or file.id is None:
                raise RuntimeError("Course note has no associated file ID")
            file_id = file.id

        with open_session() as session:
            # Commits on success and rolls back on failure.
            with session.begin():
                run = ProcessingRun(
                    celery_task_id=UUID(self.request.id),
                    task_type="lecture_processing",
                    status=ProcessingStatus.RUNNING,
                    stage=ProcessingStage.VALIDATING,
                    attempt_count=1,
                )
                session.add(run)
                session.flush()

                run_id = run.id
                if run_id is None:
                    raise RuntimeError("Processing run ID was not assigned")

                session.add(
                    LectureProcessingRun(
                        run_id=run_id,
                        note_id=note_uuid,
                    )
                )
        with processing_update(
            run_id,
            task_id=UUID(self.request.id),
            stage=ProcessingStage.VALIDATING,
        ):
            updated = LecturingProcessingState(
                **data.model_dump(), run_id=run_id, file_id=file_id
            )
            payload = updated.model_dump(mode="json")
        logger.info(
            "Preparation completed: task_id=%s run_id=%s elapsed_seconds=%.2f",
            self.request.id,
            updated.run_id,
            perf_counter() - started,
        )
        return payload

    except (Ignore, Retry, Reject):
        raise
    except Exception:
        logger.exception(
            "Failed to prepare lecture processing: "
            "task_id=%s run_id=%s course_id=%s note_id=%s",
            self.request.id,
            run_id,
            data.course_id,
            data.note_id,
        )
        raise


@app.task(bind=True, pydantic=True)
def extract_lecture_content(self: Task, data: LecturingProcessingState) -> dict:
    started = perf_counter()
    logger.info(
        "Extraction started: task_id=%s course_id=%s note_id=%s",
        self.request.id,
        data.course_id,
        data.note_id,
    )
    try:
        note_id = data.note_id
        course_id = data.course_id
        with processing_update(
            data.run_id,
            task_id=UUID(self.request.id),
            stage=ProcessingStage.DOWNLOADING,
        ), course_note_scope() as notes:
            file, content = asyncio.run(
                notes.download_note_file_strict(course_id, note_id)
            )
            if file.content_type != "application/pdf":
                raise ValueError("Only PDF files can be processed")
        with processing_update(
            data.run_id,
            task_id=UUID(self.request.id),
            stage=ProcessingStage.EXTRACTING,
        ):
            context = ExtractionContext(
                model=init_chat_model(
                    model_provider="google_genai",
                    model="gemini-3.5-flash",
                )
            )
            with TemporaryDirectory() as temp_dir:
                pdf_path = Path(temp_dir) / Path(file.original_name).name
                pdf_path.write_bytes(content)
                logger.debug(
                    "Extraction input: note_id=%s file_id=%s "
                    "content_type=%s bytes=%d path=%s",
                    note_id,
                    file.id,
                    file.content_type,
                    len(content),
                    pdf_path,
                )
                result = process_lecture(source=pdf_path, context=context)

            if result.failures:
                logger.warning(
                    "Partial extraction: note_id=%s failures=%d",
                    note_id,
                    len(result.failures),
                )
                logger.debug(
                    "Extraction failure categories: note_id=%s failures=%s",
                    note_id,
                    [
                        (failure.task, failure.section_index, failure.kind)
                        for failure in result.failures
                    ],
                )
            updated = LecturingProcessingState.model_validate(
                {
                    **data.model_dump(),
                    "extraction_result": result,
                }
            )
            payload = updated.model_dump(mode="json")
        logger.info(
            "Extraction completed: task_id=%s run_id=%s elapsed_seconds=%.2f",
            self.request.id,
            updated.run_id,
            perf_counter() - started,
        )
        return payload

    except (Ignore, Retry, Reject):
        raise
    except Exception:
        logger.exception(
            "Extraction failed: task_id=%s run_id=%s course_id=%s note_id=%s",
            self.request.id,
            data.run_id,
            data.course_id,
            data.note_id,
        )
        raise


@app.task(bind=True, pydantic=True)
def parse_and_save_note_blocks(self: Task, data: LecturingProcessingState) -> dict:
    started = perf_counter()
    logger.info(
        "Parsing and saving started: task_id=%s course_id=%s note_id=%s",
        self.request.id,
        data.course_id,
        data.note_id,
    )
    try:
        course_id = data.course_id
        file_id = data.file_id
        with processing_update(
            data.run_id,
            task_id=UUID(self.request.id),
            stage=ProcessingStage.SAVING_BLOCKS,
        ):
            if data.extraction_result is None:
                raise ValueError(
                    "Extraction result is required before parsing note blocks"
                )
            note_blocks = parse_lecture_document(
                data.extraction_result, source_file_id=file_id, course_id=course_id
            )
            with open_session() as session:
                note_block_service = NoteBlockService(session)
                saved = note_block_service.create_many(note_blocks)
                logger.info(
                    "Note blocks saved: note_id=%s count=%d", data.note_id, len(saved)
                )
                logger.debug(
                    "Saved note block IDs: note_id=%s ids=%s",
                    data.note_id,
                    [str(block.id) for block in saved],
                )
            updated = LecturingProcessingState.model_validate(
                {**data.model_dump(), "note_blocks": saved}
            )
            payload = updated.model_dump(mode="json")
        logger.info(
            "Parsing and saving completed: task_id=%s run_id=%s elapsed_seconds=%.2f",
            self.request.id,
            updated.run_id,
            perf_counter() - started,
        )
        return payload

    except (Ignore, Retry, Reject):
        raise
    except Exception:
        logger.exception(
            "Parsing and saving failed: task_id=%s run_id=%s course_id=%s note_id=%s",
            self.request.id,
            data.run_id,
            data.course_id,
            data.note_id,
        )
        raise


@app.task(bind=True, pydantic=True)
def embedd_and_save(self: Task, data: LecturingProcessingState) -> dict:
    started = perf_counter()
    logger.info(
        "Embedding and saving started: task_id=%s course_id=%s note_id=%s",
        self.request.id,
        data.course_id,
        data.note_id,
    )
    try:
        course_id = data.course_id
        note_id = data.note_id
        with processing_update(
            data.run_id,
            task_id=UUID(self.request.id),
            stage=ProcessingStage.BUILDING_DOCUMENTS,
        ):
            note_blocks = data.note_blocks
            with block_builder() as builder:
                documents = asyncio.run(builder.build(note_blocks))
                logger.info(
                    "Documents built: note_id=%s count=%d", note_id, len(documents)
                )
                if not documents:
                    logger.warning("No documents generated: note_id=%s", note_id)
        with processing_update(
            data.run_id,
            task_id=UUID(self.request.id),
            stage=ProcessingStage.INDEXING,
            final_stage=True,
        ):
            with course_vectorstore_scope() as stores:
                config = stores.get_configuration(course_id)
                if config is None:
                    config = stores.configure(
                        course_id,
                        collection_name=f"course_{course_id.hex}",
                    )
                if config.status != VectorStoreStatus.READY:
                    raise RuntimeError(
                        f"Vector-store configuration is not ready "
                        f"for course '{course_id}': {config.status}"
                    )
                logger.debug(
                    "Vector configuration: run_id=%s collection=%s namespace=%s",
                    data.run_id,
                    config.collection_name,
                    config.namespace_key,
                )
                vector_store = stores.get_vectorstore(course_id)
            vector_ids = []
            if documents:
                vector_ids = vector_store.add_documents(documents)
                logger.info(
                    "Documents indexed: run_id=%s count=%d",
                    data.run_id,
                    len(vector_ids),
                )
            updated = LecturingProcessingState.model_validate(
                {**data.model_dump(), "vector_ids": vector_ids}
            )
            payload = updated.model_dump(mode="json")
        logger.info(
            "Embedding and saving completed: task_id=%s run_id=%s elapsed_seconds=%.2f",
            self.request.id,
            updated.run_id,
            perf_counter() - started,
        )
        return payload
    except (Ignore, Retry, Reject):
        raise
    except Exception:
        logger.exception(
            "Embedding and saving failed: task_id=%s run_id=%s course_id=%s note_id=%s",
            self.request.id,
            data.run_id,
            data.course_id,
            data.note_id,
        )
        raise

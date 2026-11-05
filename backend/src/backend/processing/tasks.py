# Task return annotations such as dict | LectureProcessingState document the
# structure of the serialized state. Return model_dump(mode="json") dictionaries
# at runtime; do not rely on Celery to serialize models with union annotations.

import asyncio
from pathlib import Path
from tempfile import TemporaryDirectory
from time import perf_counter
from typing import Any
from uuid import UUID

from celery import Task
from celery.exceptions import Ignore, Reject, Retry
from langchain.chat_models import init_chat_model
from lecture_processor.api import process_lecture
from lecture_processor.graph.context import ExtractionContext, FailureConfig

from backend.core.logger import logger
from backend.courses.service.note_block_service import NoteBlockService
from backend.courses.utils import parse_lecture_document
from backend.courses.vector_store.course_vector_store_service import (
    CourseVectorStoreService,
)
from backend.database.config import open_session
from backend.processing.celery_app import app
from backend.processing.resources import (
    course_note_scope,
)

from .models import (
    LectureProcessingInput,
    LectureProcessingRun,
    LectureProcessingState,
    ProcessingRun,
    ProcessingStage,
    ProcessingStatus,
)
from .processing_run_repository import ProcessingRunRepository
from .tracking import processing_state


@app.task(bind=True, pydantic=True)
def process_lecture_file(self: Task, data: LectureProcessingInput) -> dict[str, Any]:
    started = perf_counter()
    task_id = self.request.id
    logger.info(
        "Lecture processing started: task_id=%s course_id=%s note_id=%s",
        task_id,
        data.course_id,
        data.note_id,
    )
    # Commit the run and its note association together before dispatch.
    with open_session() as session, session.begin():
        run = ProcessingRun(
            celery_task_id=UUID(self.request.id),
            task_type="lecture_processing",
            status=ProcessingStatus.STARTED,
            stage=ProcessingStage.VALIDATING,
            attempt_count=1,
        )
        run = ProcessingRunRepository(session).create(run)
        session.add(LectureProcessingRun(run_id=run.id, note_id=data.note_id))

    try:
        state = LectureProcessingState(**data.model_dump(), run_id=run.id)
        chain = (
            extract_lecture_content.s(state.model_dump(mode="json"))
            | parse_save_and_embedd.s()
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
def extract_lecture_content(self: Task, data: LectureProcessingState) -> dict:
    started = perf_counter()

    note_id = data.note_id
    with (
        processing_state(
            task=self,
            run_id=data.run_id,
            stage=ProcessingStage.DOWNLOADING,
        ),
        course_note_scope() as notes,
    ):
        file, content = asyncio.run(notes.download_note(note_id))
        if file.content_type != "application/pdf":
            raise ValueError("Only PDF files can be processed")

    with processing_state(
        task=self,
        run_id=data.run_id,
        stage=ProcessingStage.EXTRACTING,
    ):
        context = ExtractionContext(
            model=init_chat_model(
                model_provider="google_genai",
                model="gemini-3.5-flash",
            ),
            failure=FailureConfig(policy="strict"),
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

        updated = LectureProcessingState.model_validate(
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


@app.task(bind=True, pydantic=True)
def parse_save_and_embedd(
    self: Task, data: LectureProcessingState
) -> dict | LectureProcessingState:
    started = perf_counter()
    with processing_state(
        task=self, run_id=data.run_id, stage=ProcessingStage.BUILDING_DOCUMENTS
    ):
        extraction_results = data.extraction_result
        if extraction_results is None:
            raise ValueError("Extraction result is required before parsing note blocks")
        note_blocks = parse_lecture_document(
            data.extraction_result, course_note_id=data.note_id
        )
    with (
        processing_state(
            task=self, run_id=data.run_id, stage=ProcessingStage.VALIDATING
        ),
        open_session() as session,
    ):
        stores = CourseVectorStoreService(session)
        # Get vectorstore and or configure
        config = stores.get_configuration(data.course_id)
        if config is None:
            config = stores.configure(
                data.course_id,
                collection_name=f"course_{data.course_id.hex}",
            )
    with (
        processing_state(
            task=self,
            run_id=data.run_id,
            stage=ProcessingStage.INDEXING,
            final_stage=True,
        ),
        open_session() as session,
    ):
        service = NoteBlockService.from_dependencies(session, data.course_id)
        saved = asyncio.run(service.create_many(note_blocks))
        logger.info("Note blocks saved: note_id=%s count=%d", data.note_id, len(saved))
        updated = LectureProcessingState.model_validate(
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

import asyncio
from collections.abc import Generator
from contextlib import contextmanager
from pathlib import Path
from tempfile import TemporaryDirectory
from time import perf_counter
from typing import Any
from uuid import UUID

from langchain.chat_models import init_chat_model
from lecture_processor.api import process_lecture
from lecture_processor.graph.context import ExtractionContext

from backend.core.logger import logger
from backend.courses.notes.note_block_service import NoteBlockService
from backend.courses.notes.parser import parse_lecture_document
from backend.database.config import open_session
from backend.processing.celery_app import app
from backend.processing.resources import (
    block_builder,
    course_note_scope,
    course_vectorstore_scope,
)


@app.task
def process_lecture_file(course_id: str | UUID, note_id: str | UUID) -> dict[str, Any]:
    started = perf_counter()
    task_id = process_lecture_file.request.id
    logger.info(
        "Lecture processing started: task_id=%s course_id=%s note_id=%s",
        task_id,
        course_id,
        note_id,
    )
    try:
        result = _process_course_lecture_file(course_id, note_id)
        result["processing_seconds"] = perf_counter() - started
        logger.info(
            "Lecture processing succeeded: task_id=%s course_id=%s "
            "note_id=%s documents=%d elapsed_seconds=%.2f",
            task_id,
            course_id,
            note_id,
            result["document_count"],
            result["processing_seconds"],
        )
        return result
    except Exception:
        logger.exception(
            "Lecture processing failed: task_id=%s course_id=%s "
            "note_id=%s elapsed_seconds=%.2f",
            task_id,
            course_id,
            note_id,
            perf_counter() - started,
        )
        raise


@contextmanager
def _processing_stage(
    stage: str, course_id: str | UUID, note_id: str | UUID
) -> Generator[None]:
    started = perf_counter()
    task_id = process_lecture_file.request.id
    logger.info(
        "Lecture stage started: stage=%s task_id=%s course_id=%s note_id=%s",
        stage,
        task_id,
        course_id,
        note_id,
    )
    try:
        yield
    except Exception as exc:
        # The task wrapper logs the traceback once.
        logger.error(
            "Lecture stage failed: stage=%s task_id=%s course_id=%s "
            "note_id=%s error_type=%s elapsed_seconds=%.2f",
            stage,
            task_id,
            course_id,
            note_id,
            type(exc).__name__,
            perf_counter() - started,
        )
        raise
    else:
        logger.info(
            "Lecture stage completed: stage=%s task_id=%s course_id=%s "
            "note_id=%s elapsed_seconds=%.2f",
            stage,
            task_id,
            course_id,
            note_id,
            perf_counter() - started,
        )


def _process_course_lecture_file(
    course_id: str | UUID, note_id: str | UUID
) -> dict[str, Any]:
    with _processing_stage("validating_ids", course_id, note_id):
        course_uuid = course_id if isinstance(course_id, UUID) else UUID(course_id)
        note_uuid = note_id if isinstance(note_id, UUID) else UUID(note_id)
    metadata = {}
    with _processing_stage("loading_source", course_uuid, note_uuid):
        with course_note_scope() as notes:
            note = asyncio.run(notes.get_note_record(note_uuid))
            course = note.course
            if note.course_id != course_uuid:
                raise ValueError("Note does not belong to the requested course")
            file, content = asyncio.run(
                notes.download_note_file_strict(course_uuid, note_uuid)
            )
            if file.content_type != "application/pdf":
                raise ValueError("Only PDF files can be processed")

    with _processing_stage("configuring_vectorstore", course_uuid, note_uuid):
        with course_vectorstore_scope() as stores:
            config = stores.get_configuration(course_uuid)
            if config is None or not stores.is_configured(course_uuid):
                assert course.id is not None
                collection_name = f"course_{course.name}_{course.id.hex}"
                config = stores.configure(course_uuid, collection_name=collection_name)
            metadata["collection_name"] = config.collection_name
            metadata["namespace_key"] = config.namespace_key
        logger.debug(
            "Vector configuration: course_id=%s collection=%s namespace=%s",
            course_uuid,
            config.collection_name,
            config.namespace_key,
        )

    with _processing_stage("extracting", course_uuid, note_uuid):
        context = ExtractionContext(
            model=init_chat_model(
                model_provider="google_genai",
                model="gemini-2.5-flash",
            )
        )
        with TemporaryDirectory() as temp_dir:
            pdf_path = Path(temp_dir) / Path(file.original_name).name
            pdf_path.write_bytes(content)
            logger.debug(
                "Extraction input: note_id=%s file_id=%s content_type=%s bytes=%d path=%s",
                note_uuid,
                file.id,
                file.content_type,
                len(content),
                pdf_path,
            )
            result = process_lecture(source=pdf_path, context=context)
            if result.failures:
                logger.warning(
                    "Partial extraction: note_id=%s failures=%d",
                    note_uuid,
                    len(result.failures),
                )
                logger.debug(
                    "Extraction failure categories: note_id=%s failures=%s",
                    note_uuid,
                    [
                        (failure.task, failure.section_index, failure.kind)
                        for failure in result.failures
                    ],
                )

    with _processing_stage("parsing", course_uuid, note_uuid):
        note_blocks = parse_lecture_document(
            result, source_file_id=file.id, course_id=course_uuid
        )

    with _processing_stage("saving_blocks", course_uuid, note_uuid):
        with open_session() as session:
            note_block_service = NoteBlockService(session)
            saved = note_block_service.create_many(note_blocks)
            logger.info("Note blocks saved: note_id=%s count=%d", note_uuid, len(saved))
            logger.debug(
                "Saved note block IDs: note_id=%s ids=%s",
                note_uuid,
                [str(block.id) for block in saved],
            )
    with _processing_stage("building_documents", course_uuid, note_uuid):
        with block_builder() as builder:
            documents = asyncio.run(builder.build(saved))
            logger.info(
                "Documents built: note_id=%s count=%d", note_uuid, len(documents)
            )
            if not documents:
                logger.warning("No documents generated: note_id=%s", note_uuid)

    with _processing_stage("indexing", course_uuid, note_uuid):
        vector_ids = []
        if documents:
            with course_vectorstore_scope() as stores:
                vectorstore = stores.get_vectorstore(course_uuid)
                vector_ids = vectorstore.add_documents(documents)
                logger.info(
                    "Documents indexed: note_id=%s count=%d", note_uuid, len(vector_ids)
                )

    return {
        "course_id": str(course_uuid),
        "note_id": str(note_uuid),
        "vector_ids": vector_ids,
        "document_count": len(documents),
    }

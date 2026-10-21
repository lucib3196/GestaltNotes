import asyncio
from logging import getLogger
from pathlib import Path
from tempfile import TemporaryDirectory
from time import perf_counter
from typing import Any
from uuid import UUID

from langchain.chat_models import init_chat_model
from lecture_processor.api import process_lecture
from lecture_processor.graph.context import ExtractionContext

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
def process_lecture_file(course_id: str, note_id: str) -> dict[str, Any]:
    started = perf_counter()
    try:
        result = _process_course_lecture_file(course_id, note_id)
        result["processing_seconds"] = perf_counter() - started
        return result
    finally:
        getLogger(__name__).info(
            "Lecture processing finished: course_id=%s note_id=%s elapsed_seconds=%.2f",
            course_id,
            note_id,
            perf_counter() - started,
        )


def _process_course_lecture_file(course_id: str, note_id: str) -> dict[str, Any]:
    course_uuid = UUID(course_id)
    note_uuid = UUID(note_id)
    metadata = {}
    with course_note_scope() as notes:
        note = asyncio.run(notes.get_note_record(note_uuid))
        course = note.course
        if note.course_id != course_uuid:
            raise ValueError("Note does not belong to the requested course")
        file, content = asyncio.run(notes.download_note(note.file_id))
        if file.content_type != "application/pdf":
            raise ValueError("Only PDF files can be processed")

    with course_vectorstore_scope() as stores:
        config = stores.get_configuration(course_uuid)
        if config is None or not stores.is_configured(course_uuid):
            assert course.id is not None
            collection_name = f"course_{course.name}_{course.id.hex}"
            config = stores.configure(course_uuid, collection_name=collection_name)
        metadata["collection_name"] = config.collection_name
        metadata["namespace_key"] = config.namespace_key

    context = ExtractionContext(
        model=init_chat_model(
            model_provider="google_genai",
            model="gemini-2.5-flash",
        )
    )
    with TemporaryDirectory() as temp_dir:
        pdf_path = Path(temp_dir) / Path(file.original_name).name
        pdf_path.write_bytes(content)
        result = process_lecture(source=pdf_path, context=context)

    note_blocks = parse_lecture_document(
        result, source_file_id=file.id, course_id=course_uuid
    )

    with open_session() as session:
        note_block_service = NoteBlockService(session)
        saved = note_block_service.create_many(note_blocks)
    with block_builder() as builder:
        documents = asyncio.run(builder.build(saved))

    vector_ids = []
    if documents:
        with course_vectorstore_scope() as stores:
            vectorstore = stores.get_vectorstore(course_uuid)
            vector_ids = vectorstore.add_documents(documents)

    return {
        "course_id": str(course_uuid),
        "note_id": str(note_uuid),
        "vector_ids": vector_ids,
        "document_count": len(documents),
    }

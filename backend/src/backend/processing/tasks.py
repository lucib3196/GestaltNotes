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
from lecture_processor.parser.parser import (
    parse_lecture_documents,
    parse_lecture_note_blocks,
)

from backend.core import get_settings
from backend.database.config import open_session
from backend.courses.notes.models import NoteBlock
from backend.courses.notes.note_block_service import NoteBlockService
from backend.courses.vector_store.course_vector_store_service import create_vector_store
from backend.processing.celery_app import app
from backend.processing.resources import (
    file_service_scope,
    course_vectorstore_scope,
    course_note_scope,
)
from backend.processing.schema import ProcessedLecture, VectorizedLecture


async def _download_file(file_id: UUID) -> tuple[str, bytes]:
    with file_service_scope() as files:
        file, data = await files.download_file(file_id)
        if file.content_type != "application/pdf":
            raise ValueError("Only PDF files can be processed")
        return file.original_name, data


@app.task
def get_raw_lecture_output(
    file_id: str,
) -> dict[str, Any]:
    original_filename, data = asyncio.run(_download_file(UUID(file_id)))
    context = ExtractionContext(
        model=init_chat_model(
            model_provider="google_genai",
            model="gemini-2.5-flash",
        )
    )
    with TemporaryDirectory() as temp_dir:
        pdf_path = Path(temp_dir) / Path(original_filename).name
        pdf_path.write_bytes(data)
        result = process_lecture(source=pdf_path, context=context)

    return ProcessedLecture(
        file_id=file_id, file_name=original_filename, lecture=result
    ).model_dump(mode="json")


@app.task()
def vectorize_documents(payload: dict) -> dict:
    processed = ProcessedLecture.model_validate(payload)
    raw_lecture = processed.lecture
    docs = list(parse_lecture_documents(raw_lecture))
    vector_store = create_vector_store(
        collection_name=get_settings().ASTRA_DB_COLLECTION_NAME,
    )
    return VectorizedLecture(
        **payload, ids=vector_store.add_documents(docs)
    ).model_dump(mode="json")


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

    with course_note_scope() as notes:
        note = asyncio.run(notes.get_note_record(note_uuid))
        if note.course_id != course_uuid:
            raise ValueError("Note does not belong to the requested course")
        course = note.course
        file_id = note.file_id
        filename = note.file.original_name
        metadata = {
            "course_id": str(course_uuid),
            "course_name": course.name,
            "owner_id": str(course.owner_id),
            "note_id": str(note_uuid),
            "note_title": note.title,
            "resource_type": note.resource_type.value,
            "file_id": str(file_id),
            "filename": filename,
            "storage_key": note.file.storage_key,
        }
        if course.discipline is not None:
            metadata["course_discipline"] = course.discipline
        if note.file.content_type is not None:
            metadata["content_type"] = note.file.content_type

    async def download_source() -> tuple[str, bytes]:
        with file_service_scope() as files:
            file, contents = await files.download_file(file_id)
            if file.content_type != "application/pdf":
                raise ValueError("Only PDF files can be processed")
            url = await files.get_download_url(file_id)
            return url, contents

    storage_url, contents = asyncio.run(download_source())
    metadata["storage_url"] = storage_url

    with course_vectorstore_scope() as stores:
        config = stores.get_configuration(course_uuid)
        if config is None or not stores.is_configured(course_uuid):
            config = stores.create(
                course_uuid,
                collection_name=(
                    config.collection_name
                    if config is not None
                    else get_settings().ASTRA_DB_COLLECTION_NAME
                ),
            )
        metadata["namespace_key"] = config.namespace_key
        metadata["collection_name"] = config.collection_name

    context = ExtractionContext(
        model=init_chat_model(
            model_provider="google_genai",
            model="gemini-2.5-flash",
        )
    )
    with TemporaryDirectory() as temp_dir:
        pdf_path = Path(temp_dir) / Path(filename).name
        pdf_path.write_bytes(contents)
        result = process_lecture(source=pdf_path, context=context)
        pairs = list(parse_lecture_note_blocks(result))

    documents = []
    block_ids = []
    with open_session() as session:
        blocks = NoteBlockService(session)
        for index, (parsed, document) in enumerate(pairs):
            block = blocks.add(
                NoteBlock(
                    source_file_id=file_id,
                    title=parsed.title,
                    kind=parsed.kind,
                    content=parsed.content,
                )
            )
            block_id = str(block.id)
            block_ids.append(block_id)
            document.id = block_id
            document.metadata.update(metadata)
            document.metadata.update(
                note_block_id=block_id,
                title=parsed.title,
                position=index,
            )
            documents.append(document)

    vector_ids = []
    if documents:
        with course_vectorstore_scope() as stores:
            vectorstore = stores.get_vectorstore(course_uuid)
            vector_ids = vectorstore.add_documents(documents, ids=block_ids)

    return {
        "course_id": str(course_uuid),
        "note_id": str(note_uuid),
        "note_block_ids": block_ids,
        "vector_ids": vector_ids,
        "document_count": len(documents),
    }


@app.task
def update_course_docs(course_id: UUID, note_id: UUID):
    with course_note_scope() as cnotes:
        note = asyncio.run(cnotes.get_note_record(note_id))
        storage_key = note.file.storage_key
        filename = note.file.original_name
        course = note.course

    with file_service_scope() as fserv:
        url = asyncio.run(fserv.get_download_url(note.file_id))

    with course_vectorstore_scope() as vs:
        if not vs.is_configured(course_id):
            config = vs.create(
                course_id,
                collection_name=get_settings().ASTRA_DB_COLLECTION_NAME,
            )
        else:
            config = vs.get_configuration(course_id)

        assert config

        namespace = config.namespace_key
        collection_name = config.collection_name

        chunk_prefix = f"{namespace}_{filename}"

    return {
        "url": url,
        "course": course,
        "filename": filename,
        "storage_key": storage_key,
        "vs_namespace": namespace,
        "collection_name": collection_name,
        "chunk_prefix": chunk_prefix,
    }

import asyncio
from pathlib import Path
from tempfile import TemporaryDirectory
from typing import Any
from uuid import UUID

from langchain.chat_models import init_chat_model
from lecture_processor.api import process_lecture
from lecture_processor.graph.context import ExtractionContext
from lecture_processor.parser.parser import parse_lecture_documents

from backend.processing.celery_app import app
from backend.processing.resources import create_vector_store, file_service_scope
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
    vector_store = create_vector_store()
    return VectorizedLecture(
        **payload, ids=vector_store.add_documents(docs)
    ).model_dump(mode="json")


@app.task()
def process_lecture_file(data: bytes, original_name: str, file_id: UUID | str):
    context = ExtractionContext(
        model=init_chat_model(
            model_provider="google_genai",
            model="gemini-2.5-flash",
        )
    )
    with TemporaryDirectory() as temp_dir:
        pdf_path = Path(temp_dir) / Path(original_name).name
        pdf_path.write_bytes(data)
        result = process_lecture(source=pdf_path, context=context)
    return {
        "metadata": {
            "file_id": str(file_id),
            "file_name": original_name,
        },
        "raw": result.model_dump(mode="json"),
        "docs": [
            document.model_dump(mode="json")
            for document in parse_lecture_documents(result)
        ],
    }

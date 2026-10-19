"""Compatibility entry point; processing code lives in backend.processing."""

from backend.processing.celery_app import app
from backend.processing.tasks import (
    get_raw_lecture_output,
    process_lecture_file,
    vectorize_documents,
)

__all__ = [
    "app",
    "get_raw_lecture_output",
    "process_lecture_file",
    "vectorize_documents",
]

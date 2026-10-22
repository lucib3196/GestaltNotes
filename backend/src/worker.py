"""Compatibility entry point; processing code lives in backend.processing."""

from backend.processing.celery_app import app
from backend.processing.tasks import process_lecture_file

__all__ = ["app", "process_lecture_file"]

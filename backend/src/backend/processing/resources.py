from collections.abc import Generator
from contextlib import contextmanager
from time import perf_counter
from uuid import UUID

from celery.exceptions import Ignore, Reject, Retry
from object_store import BlobStorage, FirebaseBlobStorage

from backend.core import get_settings
from backend.core.exceptions import MissingConfigError
from backend.core.firebase import initialize_firebase_app
from backend.core.logger import logger
from backend.courses.notes.course_note_service import CourseNoteService
from backend.courses.notes.document_builder import NoteBlockDocumentBuilder
from backend.courses.vector_store.course_vector_store_service import (
    CourseVectorStoreService,
)
from backend.database.config import open_session
from backend.storage import FileService

from .model import (
    ProcessingStage,
    ProcessingStatus,
)
from .run_repo import RunRepo, RunUpdate


def create_storage() -> BlobStorage:
    """Initialize Firebase in the calling process before opening its bucket."""
    settings = get_settings()
    if not settings.STORAGE_BUCKET:
        raise MissingConfigError("STORAGE_BUCKET must be defined")
    initialize_firebase_app()
    return FirebaseBlobStorage(settings.STORAGE_BUCKET)


@contextmanager
def file_service_scope() -> Generator[FileService]:
    """Create a service with a fresh session and close it after use."""
    storage = create_storage()
    with open_session() as session:
        yield FileService(storage=storage, session=session)


@contextmanager
def course_vectorstore_scope() -> Generator[CourseVectorStoreService, None, None]:
    with open_session() as session:
        yield CourseVectorStoreService(session)


@contextmanager
def course_note_scope() -> Generator[CourseNoteService, None, None]:
    storage = create_storage()
    with open_session() as session:
        yield CourseNoteService(session, FileService(storage, session))


@contextmanager
def block_builder() -> Generator[NoteBlockDocumentBuilder, None, None]:
    storage = create_storage()
    with open_session() as session:
        yield NoteBlockDocumentBuilder.from_dependencies(
            session=session, storage=storage
        )


@contextmanager
def processing_update(
    run_id: UUID,
    *,
    task_id: UUID,
    stage: ProcessingStage,
    final_stage: bool = False,
) -> Generator[None]:
    """Persist stage lifecycle updates around work on an existing run."""
    started = perf_counter()

    def update_run(changes: RunUpdate) -> None:
        with open_session() as session, session.begin():
            repo = RunRepo(session)
            run = repo.get(run_id)
            if run is None:
                raise LookupError(f"Processing run '{run_id}' not found")
            repo.update(run, changes)

    logger.info(
        "Processing stage started: run_id=%s task_id=%s stage=%s",
        run_id,
        task_id,
        stage.value,
    )
    try:
        update_run(
            RunUpdate(
                status=ProcessingStatus.RUNNING,
                stage=stage,
                error_type=None,
                error_message=None,
            )
        )
        yield
        if final_stage:
            update_run(RunUpdate(status=ProcessingStatus.SUCCEEDED))
    except Retry:
        try:
            update_run(RunUpdate(status=ProcessingStatus.RETRYING, stage=stage))
        except Exception:
            logger.exception(
                "Could not persist retry status: run_id=%s task_id=%s",
                run_id,
                task_id,
            )
        logger.warning(
            "Processing stage retry requested: run_id=%s task_id=%s "
            "stage=%s elapsed_seconds=%.2f",
            run_id,
            task_id,
            stage.value,
            perf_counter() - started,
        )
        raise
    except (Ignore, Reject):
        raise
    except Exception as exc:
        logger.exception(
            "Processing stage failed: run_id=%s task_id=%s "
            "stage=%s error_type=%s elapsed_seconds=%.2f",
            run_id,
            task_id,
            stage.value,
            type(exc).__name__,
            perf_counter() - started,
        )
        try:
            update_run(
                RunUpdate(
                    status=ProcessingStatus.FAILED,
                    stage=stage,
                    error_type=type(exc).__name__,
                    error_message=f"Processing failed during {stage.value}",
                )
            )
        except Exception:
            logger.exception(
                "Could not persist failure status: run_id=%s task_id=%s",
                run_id,
                task_id,
            )
        raise
    else:
        logger.info(
            "Processing stage completed: run_id=%s task_id=%s "
            "stage=%s elapsed_seconds=%.2f",
            run_id,
            task_id,
            stage.value,
            perf_counter() - started,
        )

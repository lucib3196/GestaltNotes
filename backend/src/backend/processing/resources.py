from collections.abc import Generator
from contextlib import contextmanager
from uuid import UUID

from object_store import BlobStorage, FirebaseBlobStorage

from backend.core import get_settings
from backend.core.exceptions import MissingConfigError
from backend.core.firebase import initialize_firebase_app
from backend.courses.models import NoteBlock, NoteBlockUpdate
from backend.courses.repo.course_notes_repo import CourseNoteRepository
from backend.courses.repo.note_blocks_repo import NoteBlockRepo
from backend.courses.service.course_management import CourseManagementService
from backend.courses.service.course_note_service import CourseNoteService
from backend.courses.service.document_builder import NoteBlockDocumentBuilder
from backend.courses.service.note_block_service import NoteBlockService
from backend.courses.vector_store.course_vector_store_service import (
    CourseVectorStoreService,
)
from backend.database.config import open_session
from backend.indexer.indexer import IndexingService
from backend.processing.processing_run_repository import ProcessingRunRepository
from backend.storage import FileService


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
def course_note_scope(
    course_id: UUID,
) -> Generator[CourseNoteService, None, None]:
    """Build course-note operations with deferred indexing and a fresh session."""
    storage = create_storage()
    with open_session() as session:
        blocks = NoteBlockRepo(session)
        stores = CourseVectorStoreService(session)

        def build_indexer() -> IndexingService[NoteBlock, NoteBlockUpdate]:
            return IndexingService(
                repo=blocks,
                builder=NoteBlockDocumentBuilder(),
                vector_store=stores.get_vectorstore(course_id, async_mode=True),
            )

        yield CourseNoteService(
            session=session,
            notes=CourseNoteRepository(session),
            blocks=NoteBlockService(
                session=session,
                blocks=blocks,
                indexer_factory=build_indexer,
            ),
            access=CourseManagementService(session),
            files=FileService(storage=storage, session=session),
        )


@contextmanager
def block_builder() -> Generator[NoteBlockDocumentBuilder, None, None]:
    yield NoteBlockDocumentBuilder()


@contextmanager
def processing_run_scope() -> Generator[ProcessingRunRepository, None, None]:
    with open_session() as session:
        yield ProcessingRunRepository(session)

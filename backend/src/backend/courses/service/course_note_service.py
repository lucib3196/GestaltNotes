import asyncio
import contextlib
from dataclasses import dataclass
from pathlib import Path
from uuid import UUID, uuid4

from fastapi import UploadFile
from object_store.exceptions import BlobStorageDeleteError
from sqlmodel import Session, select

from backend.accounts import User
from backend.core.logger import logger
from backend.courses.exceptions import (
    CourseNoteAssociationError,
    CourseNoteDeletionConflictError,
    CourseNoteDeletionError,
)
from backend.courses.models import (
    Course,
    CourseContentType,
    CourseNote,
    CourseNoteRead,
    CourseNoteUpdate,
)
from backend.courses.repo import CourseNoteRepository, NoteBlockRepo
from backend.courses.service.course_access_service import CourseAccess
from backend.courses.vector_store.course_vector_store_service import (
    CourseVectorStoreService,
)
from backend.storage import FileService
from backend.storage.models import File
from backend.storage.utils import normalize_storage_key

from ..repo.lecture_processing_repo import LectureProcessingRepository


@dataclass(frozen=True, slots=True)
class FileUpload:
    filename: str
    data: bytes
    content_type: str | None = None


class CourseNoteService:
    """Coordinate course-note records, file storage, and owner checks."""

    def __init__(
        self,
        session: Session,
        notes: CourseNoteRepository,
        blocks: NoteBlockRepo,
        runs: LectureProcessingRepository,
        access: CourseAccess,
        files: FileService,
        stores: CourseVectorStoreService,
    ) -> None:
        self._session = session
        self._notes = notes
        self._blocks = blocks
        self._runs = runs
        self._access = access
        self._files = files
        self._stores = stores

    async def create(
        self,
        user: User,
        course_id: UUID,
        upload: FileUpload,
        *,
        resource_type: CourseContentType,
        title: str | None = None,
    ) -> CourseNote:
        """Upload a new file and save its note for the course owner."""
        course = await self._access.require_owner(course_id, user)
        filename = Path(upload.filename.replace("\\", "/")).name.strip()
        if not filename or filename in {".", ".."}:
            raise ValueError("Filename is required")
        if not upload.data:
            raise ValueError("File must not be empty")
        storage_key = normalize_storage_key(
            course.storage_prefix, "notes", uuid4().hex, filename
        )
        try:
            file = await self._files.stage_file(
                user,
                filename=storage_key,
                data=upload.data,
                content_type=upload.content_type,
            )
            note = await self._notes.create(
                self._create_note_record(
                    course,
                    file,
                    resource_type=resource_type,
                    title=title if title is not None else filename,
                )
            )
            self._session.commit()
            return note
        except Exception:
            self._session.rollback()
            with contextlib.suppress(BlobStorageDeleteError):
                await self._delete_blob_with_retry(storage_key)
            raise

    async def upload(
        self,
        user: User,
        course_id: UUID,
        upload: UploadFile,
        resource_type: CourseContentType,
        *,
        title: str | None = None,
    ) -> CourseNote:
        """Adapt an HTTP upload to the course-note creation operation."""
        # Authorize before reading the upload into memory.
        await self._access.require_owner(course_id, user)
        if not upload.filename:
            raise ValueError("Filename is required")
        return await self.create(
            user,
            course_id,
            FileUpload(upload.filename, await upload.read(), upload.content_type),
            resource_type=resource_type,
            title=title,
        )

    async def update(
        self,
        note_id: UUID,
        update: CourseNoteUpdate,
        *,
        user: User,
    ) -> CourseNote:
        """Save note metadata after checking course ownership."""
        note = await self._notes.get_required(note_id)
        await self._access.require_owner(note.course_id, user)
        if any(
            value is None for value in update.model_dump(exclude_unset=True).values()
        ):
            raise ValueError("Note title and resource type cannot be null")
        try:
            note = await self._notes.update(note, update)
            self._session.commit()
            return note
        except Exception:
            self._session.rollback()
            raise

    async def delete(self, note_id: UUID, *, user: User) -> None:
        """Remove vectors, commit note/file deletion, then remove the stored blob."""
        note = await self._notes.get_required(note_id)
        await self._access.require_owner(note.course_id, user)

        active_run = self._runs.get_latest_active(note_id)
        if active_run is not None:
            raise CourseNoteDeletionConflictError(
                "This file is being processed. "
                "Wait for processing to finish before deleting it."
            )

        # Deleting the physical file cascades to every attachment. Avoid
        # removing another course's resource through this note-scoped action.
        shared_note = self._session.exec(
            select(CourseNote).where(
                CourseNote.file_id == note.file_id, CourseNote.id != note_id
            )
        ).first()
        if shared_note is not None:
            raise CourseNoteDeletionConflictError(
                "This file is attached to another course note "
                "and cannot be deleted here."
            )

        blocks = await self._blocks.list_by_note(note_id)
        if blocks:
            store = self._stores.get_vectorstore(note.course_id, async_mode=True)
            try:
                result = await store.adelete(ids=[str(block.id) for block in blocks])
                if result is False:
                    raise RuntimeError("Vector deletion was not acknowledged")
            except Exception as exc:
                logger.exception("Embedding cleanup failed: note_id=%s", note_id)
                raise CourseNoteDeletionError(
                    "Could not remove this file's embeddings. "
                    "The file has not been deleted."
                ) from exc

        try:
            file_id = note.file_id
            await self._notes.delete(note_id)
            file = await self._files.stage_delete_file(file_id)
            storage_key = file.storage_key
            self._session.commit()
        except Exception:
            self._session.rollback()
            raise
        # Database deletion is already committed; a blob failure cannot roll it back.
        try:
            await self._delete_blob_with_retry(storage_key)
        except BlobStorageDeleteError as exc:
            raise CourseNoteDeletionError(
                "Lecture materials were removed, but deleting the stored file failed. "
                "Refresh the list."
            ) from exc

    async def _delete_blob_with_retry(self, storage_key: str) -> None:
        """Retry temporary storage deletion failures up to three attempts."""
        for attempt in range(3):
            try:
                await self._files.delete_blob(storage_key)
                return
            except BlobStorageDeleteError:
                if attempt == 2:
                    logger.exception("Blob cleanup failed: storage_key=%s", storage_key)
                    raise
                await asyncio.sleep(0.1 * (2**attempt))

    async def upload_note(
        self,
        course_id: UUID,
        educator: User,
        upload: UploadFile,
        resource_type: CourseContentType,
        title: str | None = None,
    ) -> CourseNote:
        """Preserve the existing upload interface for route callers."""
        return await self.upload(
            educator,
            course_id,
            upload,
            resource_type,
            title=title,
        )

    async def update_note_properties(
        self,
        note_id: UUID,
        update: CourseNoteUpdate,
        *,
        user: User,
    ) -> CourseNote:
        """Delegate metadata updates through the owner-checked operation."""
        return await self.update(note_id, update, user=user)

    async def remove_note(self, note_id: UUID, educator: User) -> None:
        """Preserve the existing owner-checked note deletion interface."""
        await self.delete(note_id, user=educator)

    async def assert_permission(self, educator: User, note_id: UUID) -> None:
        """Require ownership of the course containing the note."""
        note = await self._notes.get_required(note_id)
        await self._access.require_owner(note.course_id, educator)

    async def add_file(
        self,
        course: Course,
        file: File,
        *,
        resource_type: CourseContentType = CourseContentType.OTHER,
        title: str | None = None,
    ) -> CourseNote:
        """Attach an existing file for trusted internal callers; no access check."""
        try:
            note = await self._notes.create(
                self._create_note_record(
                    course,
                    file,
                    resource_type=resource_type,
                    title=title,
                )
            )
            self._session.commit()
            return note
        except Exception:
            self._session.rollback()
            raise

    async def remove_file(self, note_id: UUID) -> None:
        """Detach a note for trusted internal callers, retaining its file."""
        try:
            await self._notes.delete(note_id)
            self._session.commit()
        except Exception:
            self._session.rollback()
            raise

    async def get_note_record(self, note_id: UUID) -> CourseNote:
        return await self._notes.get_required(note_id)

    async def get_note(self, note_id: UUID) -> CourseNoteRead:
        return await self._notes.get_note_read(note_id)

    def to_note_read(self, note: CourseNote) -> CourseNoteRead:
        return self._notes.to_note_read(note)

    async def list_notes(self, course_id: UUID) -> list[CourseNote]:
        return await self._notes.list_by_course(course_id)

    async def list_notes_with_urls(self, course_id: UUID) -> list[CourseNoteRead]:
        notes = await self._notes.list_by_course(course_id)
        return [self._notes.to_note_read(note) for note in notes]

    async def download_note(self, note_id: UUID) -> tuple[File, bytes]:
        note = await self._notes.get_required(note_id)
        return await self._files.download_file(note.file_id)

    def _create_note_record(
        self,
        course: Course,
        file: File,
        *,
        resource_type: CourseContentType,
        title: str | None,
    ) -> CourseNote:
        if not course.id:
            raise CourseNoteAssociationError("Cannot add file to course without id")
        if not file.id:
            raise CourseNoteAssociationError("Cannot add file without id")

        return CourseNote(
            course_id=course.id,
            file_id=file.id,
            resource_type=resource_type,
            title=title or file.original_name,
        )

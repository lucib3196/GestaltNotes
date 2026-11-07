import asyncio
import contextlib
from dataclasses import dataclass
from pathlib import Path
from uuid import UUID, uuid4

from fastapi import UploadFile
from object_store.exceptions import BlobStorageDeleteError
from sqlmodel import Session

from backend.accounts import User
from backend.core.logger import logger
from backend.courses.exceptions import (
    CourseNoteAssociationError,
    CourseNoteDeletionError,
)
from backend.courses.models import (
    Course,
    CourseContentType,
    CourseNote,
    CourseNoteRead,
    CourseNoteUpdate,
)
from backend.courses.repo.course_notes_repo import CourseNoteRepository
from backend.courses.service.course_access_service import CourseAccess
from backend.courses.service.note_block_service import NoteBlockService
from backend.storage import FileService
from backend.storage.models import File
from backend.storage.utils import normalize_storage_key


@dataclass(frozen=True, slots=True)
class FileUpload:
    filename: str
    data: bytes
    content_type: str | None = None


class CourseNoteService:
    """Manage course-note records, associated files, and block cleanup.

    Creation, updates, and full deletion enforce course ownership. Read and
    attachment operations rely on trusted callers to authorize access.
    Delegate block and vector deletion to NoteBlockService.
    """

    def __init__(
        self,
        session: Session,
        files: FileService,
        notes: CourseNoteRepository,
        blocks: NoteBlockService,
        access: CourseAccess,
    ) -> None:
        self._session = session
        self._notes = notes
        self._blocks = blocks
        self._access = access
        self._files = files

    async def list_notes(self, course_id: UUID) -> list[CourseNote]:
        """List a course's notes; callers must authorize access."""
        return await self._notes.list_by_course(course_id)

    async def download_note(self, note_id: UUID) -> tuple[File, bytes]:
        """Download a note's file and metadata; callers must authorize access."""
        note = await self._notes.get_required(note_id)
        return await self._files.download_file(note.file_id)

    def to_note_read(self, note: CourseNote) -> CourseNoteRead:
        """Convert a note into its public response representation."""
        return self._notes.to_note_read(note)

    async def create(
        self,
        user: User,
        course_id: UUID,
        upload: FileUpload,
        *,
        resource_type: CourseContentType,
        title: str | None = None,
    ) -> CourseNote:
        """Upload a file and commit its note after verifying course ownership.

        Roll back database changes and attempt blob cleanup if creation fails."""
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
        """Authorize and read an HTTP upload, then delegate to create."""
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
        """Authorize and commit note metadata changes; roll back on failure."""
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
        """Authorize, remove block vectors and rows, then delete the note and file.

        Commit database deletion before removing the blob. Database rollback
        cannot restore vectors; blob failure cannot undo the committed deletion."""
        note = await self._notes.get_required(note_id)
        await self._access.require_owner(note.course_id, user)

        try:
            file_id = note.file_id
            # Keep source records available until vector cleanup finishes.
            await self._blocks.delete_by_note_id(note_id, commit=False)
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

    async def add_file(
        self,
        course: Course,
        file: File,
        *,
        resource_type: CourseContentType = CourseContentType.OTHER,
        title: str | None = None,
    ) -> CourseNote:
        """Commit an attachment to an existing file for trusted internal callers.

        Does not upload a blob or perform an ownership check."""
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
        """Commit note detachment while retaining the file record and blob.

        For trusted internal callers; does not explicitly clean vector documents."""
        try:
            await self._notes.delete(note_id)
            self._session.commit()
        except Exception:
            self._session.rollback()
            raise

    def _create_note_record(
        self,
        course: Course,
        file: File,
        *,
        resource_type: CourseContentType,
        title: str | None,
    ) -> CourseNote:
        """Build a note association after checking course and file IDs."""
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

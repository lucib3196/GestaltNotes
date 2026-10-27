import contextlib
from uuid import UUID

from fastapi import UploadFile
from object_store.exceptions import BlobStorageDeleteError
from sqlmodel import Session

from backend.accounts import User
from backend.courses.exceptions import (
    CourseNoteAssociationError,
)
from backend.courses.models import Course
from backend.courses.notes.models import CourseContentType, CourseNote
from backend.courses.notes.repo import CourseNoteRepository
from backend.courses.notes.schema import CourseNoteRead, CourseNoteUpdate
from backend.courses.service.course_service import CourseService
from backend.storage import FileService
from backend.storage.models import File
from backend.storage.utils import normalize_storage_key


class CourseNoteService:
    def __init__(
        self,
        session: Session,
        file_service: FileService,
    ) -> None:
        self._session = session
        self._files = file_service
        self._courses = CourseService(session)
        self._repo = CourseNoteRepository(session)

    async def upload_note(
        self,
        course_id: UUID,
        educator: User,
        upload: UploadFile,
        resource_type: CourseContentType,
        title: str | None = None,
    ) -> CourseNote:
        course = await self._courses.assert_course_owner(course_id, educator)
        contents = await upload.read()

        if not upload.filename:
            raise ValueError("Failed to determine filename")

        storage_key = normalize_storage_key(
            course.storage_prefix,
            "notes",
            upload.filename,
        )

        try:
            file_record = await self._files.stage_file(
                owner=educator,
                filename=storage_key,
                data=contents,
                content_type=upload.content_type,
            )
            note = await self._repo.create(
                self._create_note_record(
                    course=course,
                    file=file_record,
                    resource_type=resource_type,
                    title=title,
                )
            )
            self._session.commit()
            return note
        except Exception:
            self._session.rollback()
            with contextlib.suppress(BlobStorageDeleteError):
                await self._files.delete_blob(storage_key)
            raise

    async def add_file(
        self,
        course: Course,
        file: File,
        *,
        resource_type: CourseContentType = CourseContentType.OTHER,
        title: str | None = None,
    ) -> CourseNote:
        try:
            note = await self._repo.create(
                self._create_note_record(
                    course=course,
                    file=file,
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
        """Remove the note association while retaining its stored file."""
        await self._repo.get_required(note_id)
        try:
            await self._repo.delete(note_id)
            self._session.commit()
        except Exception:
            self._session.rollback()
            raise

    async def remove_note(self, note_id: UUID, educator: User) -> None:
        note = await self._repo.get_required(note_id)
        await self._courses.assert_course_owner(note.course_id, educator)

        try:
            file = await self._files.stage_delete_file(note.file_id)
            await self._repo.delete(note_id)
            self._session.commit()
        except Exception:
            self._session.rollback()
            raise
        await self._files.delete_blob(file.storage_key)

    async def get_note_record(self, note_id: UUID) -> CourseNote:
        return await self._repo.get_required(note_id)

    async def get_note(self, note_id: UUID) -> CourseNoteRead:
        return await self._repo.get_note_read(note_id)

    def to_note_read(self, note: CourseNote) -> CourseNoteRead:
        return self._repo.to_note_read(note)

    async def list_notes(self, course_id: UUID) -> list[CourseNote]:
        return await self._repo.list_by_course(course_id)

    async def list_notes_with_urls(self, course_id: UUID) -> list[CourseNoteRead]:
        notes = await self._repo.list_by_course(course_id)
        return [self._repo.to_note_read(note) for note in notes]

    async def download_note(self, note_id: UUID) -> tuple[File, bytes]:
        note = await self._repo.get_required(note_id)
        return await self._files.download_file(note.file_id)

    async def update_note_properties(
        self, note_id: UUID, update: CourseNoteUpdate
    ) -> CourseNote:
        note = await self._repo.get_required(note_id)
        return await self._repo.update(note, update)

    async def assert_permission(self, educator: User, note_id: UUID) -> None:
        note = await self._repo.get_required(note_id)
        await self._courses.assert_course_owner(note.course_id, educator)

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

import contextlib
from uuid import UUID

from fastapi import UploadFile
from sqlmodel import Session

from backend.accounts import User
from backend.courses.exceptions import (
    CourseNoteAssociationError,
    CourseNoteNotFoundError,
)
from backend.courses.models import Course, CourseContentType, CourseNote
from backend.courses.notes.repo import CourseNoteRepository
from backend.courses.schema import CourseNoteRead
from backend.courses.service.course_service import CourseService
from backend.storage import FileService
from backend.storage.blob.exceptions import BlobStorageDeleteError
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

    async def remove_file(
        self,
        course_id: UUID,
        file_id: UUID,
    ) -> None:
        try:
            note = await self._repo.get_by_course_and_file(course_id, file_id)

            if note is None or note.id is None:
                raise CourseNoteNotFoundError(str(course_id), str(file_id))

            await self._repo.delete(note.id)
            self._session.commit()
        except Exception:
            self._session.rollback()
            raise

    async def remove_note(
        self,
        course_id: UUID,
        note_id: UUID,
        educator: User,
    ) -> None:
        await self._courses.assert_course_owner(course_id, educator)

        note = await self._repo.get(note_id)
        if note is None or note.id is None or note.course_id != course_id:
            raise CourseNoteNotFoundError(str(course_id), str(note_id))

        try:
            file = await self._files.stage_delete_file(note.file_id)
            await self._repo.delete(note.id)
            self._session.commit()
        except Exception:
            self._session.rollback()
            raise
        await self._files.delete_blob(file.storage_key)

    async def list_notes(self, course_id: UUID) -> list[CourseNote]:
        return await self._repo.list_by_course(course_id)

    async def read_note(self, note: CourseNote) -> CourseNoteRead:
        download_url = await self._files.get_download_url(note.file_id)
        if not note.id:
            raise CourseNoteAssociationError("Cannot read note without id")

        return CourseNoteRead(
            id=note.id,
            course_id=note.course_id,
            file_id=note.file_id,
            title=note.title,
            resource_type=note.resource_type,
            download_url=download_url,
        )

    async def list_notes_with_urls(self, course_id: UUID) -> list[CourseNoteRead]:
        notes = await self.list_notes(course_id)
        return [await self.read_note(note) for note in notes]

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

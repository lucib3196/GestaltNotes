from uuid import UUID
from sqlalchemy.exc import SQLAlchemyError
from backend.src.backend.courses.models import CourseContentType
from fastapi import UploadFile
from sqlmodel import Session
from backend.accounts import User
from backend.courses.models import CourseNote
from backend.storage import FileService
from backend.storage.utils import normalize_storage_key

from .course_note_service import CourseNoteService
from backend.courses.service.course_service import CourseService


class CourseNoteManager:
    def __init__(self, file_service: FileService, session: Session) -> None:
        self._session = session
        self._files = file_service
        self._courses = CourseService(self._session)
        self._notes = CourseNoteService(self._session)

    async def upload_course_note(
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
            course.storage_prefix, "notes", upload.filename
        )
        try:
            file_record = await self._files.stage_file(
                owner=educator,
                filename=storage_key,
                data=contents,
                content_type=upload.content_type,
            )
            note = await self._notes.stage_file_for_course(
                course=course,
                file=file_record,
                resource_type=resource_type,
                title=title,
            )
            self._session.commit()
            return note
        except SQLAlchemyError as e:
            self._session.rollback()
            raise ValueError(f"Failed to upload note {e}")

    async def remove_course_note(
        self,
        course_id: UUID,
        note_id: UUID,
        educator: User,
    ) -> None:
        course = await self._courses.assert_course_owner(course_id, educator)
        note = self._notes.get_note(note_id)
        assert note
        assert note.id
        try:
            await self._notes.stage_remove_course_note(note.id)
            await self._files.stage_delete_file(note.file_id)
            return None
        except Exception as e:
            raise e

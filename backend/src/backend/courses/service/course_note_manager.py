import fastapi
from backend.src.backend.courses.models import CourseContentType
from backend.tests.integration.storage.test_file_repository import storage_key
from .course_service import CourseService
from backend.storage import FileService
from .course_note_service import CourseNoteService
from uuid import UUID
from fastapi import UploadFile
from backend.courses.models import CourseNote
from backend.accounts import User
from backend.storage.utils import normalize_storage_key


class CourseNoteManager:
    def __init__(
        self,
        course_service: CourseService,
        file_service: FileService,
        course_note_service: CourseNoteService,
    ) -> None:
        self._courses = course_service
        self._files = file_service
        self._notes = course_note_service

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
        file_record = await self._files.create_file(
            owner=educator,
            filename=storage_key,
            data=contents,
            content_type=upload.content_type,
        )
        return await self._notes.add_file_to_course(
            course=course,
            file=file_record,
            resource_type=resource_type,
            title=title,
        )

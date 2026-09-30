from uuid import UUID

from fastapi import File, UploadFile
from fastapi.routing import APIRouter
from starlette import status

from backend.courses.exceptions import CourseServiceException
from backend.courses.models import CourseContentType
from backend.courses.schema import CourseNoteDelete, CourseNoteRead
from backend.web.accounts.dependencies import EducatorDep
from backend.web.courses.dependencies import CourseNoteServiceDep
from backend.web.courses.http import course_http_exception

ID = UUID | str

router = APIRouter(prefix="/courses/notes", tags=["courses", "notes"])


@router.get("/{course_id}", response_model=list[CourseNoteRead])
async def list_course_notes(
    course_id: UUID,
    service: CourseNoteServiceDep,
):
    try:
        return await service.list_notes_with_urls(course_id)
    except CourseServiceException as e:
        raise course_http_exception(e) from e


@router.post(
    "/{course_id}",
    response_model=CourseNoteRead,
    status_code=status.HTTP_201_CREATED,
)
async def upload_course_note(
    course_id: UUID,
    educator: EducatorDep,
    service: CourseNoteServiceDep,
    file: UploadFile = File(...),
):
    try:
        note = await service.upload_note(
            course_id=course_id,
            educator=educator,
            upload=file,
            resource_type=CourseContentType.NOTES,
        )
        return await service.read_note(note)
    except CourseServiceException as e:
        raise course_http_exception(e) from e


@router.delete("/{course_id}/{note_id}", response_model=CourseNoteDelete)
async def remove_course_note(
    course_id: UUID,
    note_id: UUID,
    educator: EducatorDep,
    service: CourseNoteServiceDep,
) -> CourseNoteDelete:
    try:
        await service.remove_note(course_id, note_id, educator)
        return CourseNoteDelete(success=True, info="Course note deleted.")
    except CourseServiceException as e:
        raise course_http_exception(e) from e

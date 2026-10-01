from io import BytesIO
from uuid import UUID

from fastapi import File, Form, UploadFile
from fastapi.responses import StreamingResponse
from fastapi.routing import APIRouter
from starlette import status

from backend.courses.exceptions import CourseServiceException
from backend.courses.models import CourseContentType
from backend.courses.schema import CourseNoteDelete, CourseNoteRead
from backend.web.accounts.dependencies import CurrentUserDep, EducatorDep
from backend.web.courses.dependencies import CourseNoteServiceDep
from backend.web.courses.http import course_http_exception
from backend.courses.schema import CourseNoteUpdate

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
    resource_type: CourseContentType = Form(CourseContentType.NOTES),
):
    try:
        note = await service.upload_note(
            course_id=course_id,
            educator=educator,
            upload=file,
            resource_type=resource_type,
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


@router.put("/{course_id}/{note_id}", response_model=CourseNoteRead)
async def update_course_note(
    course_id: UUID,
    note_id: UUID,
    educator: EducatorDep,
    service: CourseNoteServiceDep,
    update: CourseNoteUpdate,
):
    try:
        await service.assert_permission(educator, course_id)
        return await service.update_note_properties(course_id, note_id, update)
    except Exception as e:
        raise ValueError("Failed")


@router.get("/{course_id}/{note_id}/stream")
async def stream_course_note(
    course_id: UUID,
    note_id: UUID,
    _user: CurrentUserDep,
    service: CourseNoteServiceDep,
)->StreamingResponse:
    try:
        file, data = await service.download_note_file(
            course_id=course_id,
            note_id=note_id,
        )
        return StreamingResponse(
            BytesIO(data),
            media_type=file.content_type or "application/octet-stream",
            headers={
                "Content-Disposition": f'inline; filename="{file.original_name}"',
            },
        )
    except CourseServiceException as e:
        raise course_http_exception(e) from e

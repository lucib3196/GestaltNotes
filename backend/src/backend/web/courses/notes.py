from io import BytesIO
from uuid import UUID

from fastapi import File, Form, UploadFile
from fastapi.responses import StreamingResponse
from fastapi.routing import APIRouter
from starlette import status

from backend.courses.exceptions import CourseServiceException
from backend.courses.notes.models import CourseContentType
from backend.courses.notes.schema import (
    CourseNoteDelete,
    CourseNoteRead,
    CourseNoteUpdate,
    NoteOverview,
)
from backend.web.accounts.dependencies import CurrentUserDep, EducatorDep
from backend.web.courses.dependencies import (
    CourseNoteProcessingServiceDep,
    CourseNoteServiceDep,
    ReadableCourseDep,
    ReadableCourseNoteDep,
)
from backend.web.courses.http import course_http_exception

router = APIRouter(prefix="/courses/notes", tags=["courses", "notes"])


@router.get("/{course_id}", response_model=list[CourseNoteRead])
async def list_course_notes(
    course_id: UUID,
    service: CourseNoteServiceDep,
) -> list[CourseNoteRead]:
    try:
        return await service.list_notes_with_urls(course_id)
    except CourseServiceException as e:
        raise course_http_exception(e) from e


@router.get("/{course_id}/overview", response_model=list[NoteOverview])
async def list_course_note_overview(
    course_id: UUID,
    processing: CourseNoteProcessingServiceDep,
    _course: ReadableCourseDep,
) -> list[NoteOverview]:
    try:
        return await processing.list_notes_overview(course_id)
    except CourseServiceException as e:
        raise course_http_exception(e) from e


@router.get("/{course_id}/{note_id}/overview", response_model=NoteOverview)
async def get_note_overview(
    course_id: UUID,
    note_id: UUID,
    educator: CurrentUserDep,
    service: CourseNoteServiceDep,
    processing: CourseNoteProcessingServiceDep,
    _note: ReadableCourseNoteDep,
) -> NoteOverview:
    try:
        await service.assert_permission(educator, note_id)
        return await processing.get_note_overview(note_id)
    except CourseServiceException as e:
        raise course_http_exception(e) from e


@router.get("/{course_id}/{note_id}/stream")
async def stream_course_note(
    course_id: UUID,
    note_id: UUID,
    _user: CurrentUserDep,
    service: CourseNoteServiceDep,
    _note: ReadableCourseNoteDep,
) -> StreamingResponse:
    try:
        file, data = await service.download_note(note_id)
        return StreamingResponse(
            BytesIO(data),
            media_type=file.content_type or "application/octet-stream",
            headers={
                "Content-Disposition": f'inline; filename="{file.original_name}"',
            },
        )
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
) -> CourseNoteRead:
    try:
        note = await service.upload_note(
            course_id=course_id,
            educator=educator,
            upload=file,
            resource_type=resource_type,
        )
        return service.to_note_read(note)
    except CourseServiceException as e:
        raise course_http_exception(e) from e


@router.put("/{course_id}/{note_id}", response_model=CourseNoteRead)
async def update_course_note(
    course_id: UUID,
    note_id: UUID,
    educator: EducatorDep,
    service: CourseNoteServiceDep,
    _note: ReadableCourseNoteDep,
    update: CourseNoteUpdate,
) -> CourseNoteRead:
    try:
        await service.assert_permission(educator, note_id)
        note = await service.update_note_properties(note_id, update)
        return service.to_note_read(note)
    except CourseServiceException as e:
        raise course_http_exception(e) from e


@router.delete("/{course_id}/{note_id}", response_model=CourseNoteDelete)
async def remove_course_note(
    course_id: UUID,
    note_id: UUID,
    educator: EducatorDep,
    service: CourseNoteServiceDep,
    _note: ReadableCourseNoteDep,
) -> CourseNoteDelete:
    try:
        await service.remove_note(note_id, educator)
        return CourseNoteDelete(success=True, info="Course note deleted.")
    except CourseServiceException as e:
        raise course_http_exception(e) from e

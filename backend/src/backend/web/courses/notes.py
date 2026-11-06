from io import BytesIO
from typing import Annotated
from uuid import UUID

from fastapi import File, Form, HTTPException, UploadFile
from fastapi.responses import StreamingResponse
from fastapi.routing import APIRouter
from starlette import status

from backend.courses.exceptions import CourseServiceException
from backend.courses.models import (
    CourseContentType,
    CourseNoteDelete,
    CourseNoteRead,
    CourseNoteUpdate,
    NoteOverview,
)
from backend.web.accounts.dependencies import CurrentUserDep, EducatorDep
from backend.web.courses.dependencies import (
    CourseNoteProcessingServiceDep,
    CourseNoteServiceDep,
    OwnedCourseNoteDep,
    ReadableCourseDep,
    ReadableCourseNoteDep,
)
from backend.web.courses.http import course_http_exception

router = APIRouter(prefix="/courses/notes", tags=["courses", "notes"])


@router.get("/{course_id}", response_model=list[CourseNoteRead])
async def list_course_notes(
    course_id: UUID,
    service: CourseNoteServiceDep,
    _course: ReadableCourseDep,
) -> list[CourseNoteRead]:
    try:
        notes = await service.list_notes(course_id)
        return [service.to_note_read(note) for note in notes]
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
    note_id: UUID,
    processing: CourseNoteProcessingServiceDep,
    _note: ReadableCourseNoteDep,
) -> NoteOverview:
    try:
        return await processing.get_note_overview(note_id)
    except CourseServiceException as e:
        raise course_http_exception(e) from e


@router.get("/{course_id}/{note_id}/stream")
async def stream_course_note(
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
    file: Annotated[UploadFile, File()],
    resource_type: Annotated[CourseContentType, Form()] = CourseContentType.NOTES,
) -> CourseNoteRead:
    try:
        note = await service.upload(
            course_id=course_id,
            user=educator,
            upload=file,
            resource_type=resource_type,
        )
        return service.to_note_read(note)
    except ValueError as exc:
        raise HTTPException(status_code=422, detail=str(exc)) from exc
    except CourseServiceException as e:
        raise course_http_exception(e) from e


@router.patch("/{course_id}/{note_id}", response_model=CourseNoteRead)
@router.put("/{course_id}/{note_id}", response_model=CourseNoteRead, deprecated=True)
async def update_course_note(
    note_id: UUID,
    educator: EducatorDep,
    service: CourseNoteServiceDep,
    _note: OwnedCourseNoteDep,
    update: CourseNoteUpdate,
) -> CourseNoteRead:
    try:
        note = await service.update(note_id, update, user=educator)
        return service.to_note_read(note)
    except ValueError as exc:
        raise HTTPException(status_code=422, detail=str(exc)) from exc
    except CourseServiceException as e:
        raise course_http_exception(e) from e


@router.delete("/{course_id}/{note_id}", response_model=CourseNoteDelete)
async def remove_course_note(
    note_id: UUID,
    educator: EducatorDep,
    service: CourseNoteServiceDep,
    _note: OwnedCourseNoteDep,
) -> CourseNoteDelete:
    try:
        await service.delete(note_id, user=educator)
        return CourseNoteDelete(success=True, info="Course note deleted.")
    except CourseServiceException as e:
        raise course_http_exception(e) from e


@router.get("/{course_id}/{note_id}", response_model=CourseNoteRead)
async def get_course_note(
    note: ReadableCourseNoteDep,
) -> CourseNoteRead:
    """Read one authorized resource without storage or embedding dependencies."""
    return CourseNoteRead(
        id=note.id,
        course_id=note.course_id,
        file_id=note.file_id,
        title=note.title,
        resource_type=note.resource_type,
        content_type=note.file.content_type if note.file else None,
    )

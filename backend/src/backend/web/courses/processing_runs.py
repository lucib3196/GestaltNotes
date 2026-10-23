from uuid import UUID

from fastapi import HTTPException
from fastapi.routing import APIRouter

from backend.courses.exceptions import CourseNoteNotFoundError
from backend.processing.exceptions import (
    LectureProcessingRunNotFoundError,
)
from backend.processing.models import ProcessingRun
from backend.processing.schema import LectureProcessingStatusRead, ProcessingRunRead

from .dependencies import CourseNoteProcessingServiceDep, ReadableCourseNoteDep

router = APIRouter(
    prefix="/courses/notes/{course_id}/{note_id}",
    tags=["courses", "processing runs"],
)


@router.get(
    "/runs",
    response_model=list[ProcessingRunRead],
)
async def list_processing_runs(
    note_id: UUID,
    service: CourseNoteProcessingServiceDep,
    _note: ReadableCourseNoteDep,
) -> list[ProcessingRun]:
    try:
        return await service.list_runs(note_id)
    except CourseNoteNotFoundError as exc:
        raise HTTPException(404, str(exc)) from exc


@router.get(
    "/runs/{run_id}",
    response_model=ProcessingRunRead,
)
async def get_processing_run(
    note_id: UUID,
    run_id: UUID,
    service: CourseNoteProcessingServiceDep,
    _note: ReadableCourseNoteDep,
) -> ProcessingRun:
    try:
        return await service.get_run(note_id, run_id)
    except (
        CourseNoteNotFoundError,
        LectureProcessingRunNotFoundError,
    ) as exc:
        raise HTTPException(404, str(exc)) from exc


@router.get(
    "/status",
    response_model=LectureProcessingStatusRead,
)
async def get_processing_status(
    note_id: UUID,
    service: CourseNoteProcessingServiceDep,
    _note: ReadableCourseNoteDep,
) -> LectureProcessingStatusRead:
    try:
        return await service.get_processing_status(note_id)
    except CourseNoteNotFoundError as exc:
        raise HTTPException(404, str(exc)) from exc

from uuid import UUID

from fastapi import HTTPException
from fastapi.routing import APIRouter

from backend.processing.exceptions import (
    LectureProcessingNoteNotFoundError,
    LectureProcessingRunNotFoundError,
)
from backend.processing.models import ProcessingRun
from backend.processing.schema import LectureProcessingStatusRead, ProcessingRunRead
from backend.web.courses.dependencies import ReadableCourseDep

from .dependencies import LectureProcessingServiceDep

router = APIRouter(prefix="/tasks", tags=["tasks"])


@router.get(
    "/course/{course_id}/{note_id}/runs",
    response_model=list[ProcessingRunRead],
)
def list_processing_runs(
    course_id: UUID,
    note_id: UUID,
    service: LectureProcessingServiceDep,
    _course: ReadableCourseDep,
) -> list[ProcessingRun]:
    try:
        return service.list_runs(course_id, note_id)
    except LectureProcessingNoteNotFoundError as exc:
        raise HTTPException(404, str(exc)) from exc


@router.get(
    "/course/{course_id}/{note_id}/runs/{run_id}",
    response_model=ProcessingRunRead,
)
def get_processing_run(
    course_id: UUID,
    note_id: UUID,
    run_id: UUID,
    service: LectureProcessingServiceDep,
    _course: ReadableCourseDep,
) -> ProcessingRun:
    try:
        return service.get_run(course_id, note_id, run_id)
    except (
        LectureProcessingNoteNotFoundError,
        LectureProcessingRunNotFoundError,
    ) as exc:
        raise HTTPException(404, str(exc)) from exc


@router.get(
    "/course/{course_id}/{note_id}/status",
    response_model=LectureProcessingStatusRead,
)
def get_processing_status(
    course_id: UUID,
    note_id: UUID,
    service: LectureProcessingServiceDep,
    _course: ReadableCourseDep,
) -> LectureProcessingStatusRead:
    try:
        return service.get_processing_status(course_id, note_id)
    except LectureProcessingNoteNotFoundError as exc:
        raise HTTPException(404, str(exc)) from exc

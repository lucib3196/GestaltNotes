from uuid import UUID

from fastapi import HTTPException
from fastapi.routing import APIRouter

from backend.database import SessionDep
from backend.processing.exceptions import (
    LectureProcessingNoteNotFoundError,
    LectureProcessingRunNotFoundError,
)
from backend.processing.lecture_processing_service import LectureProcessingService
from backend.processing.models import ProcessingRun
from backend.processing.schema import ProcessingRunRead
from backend.web.courses.dependencies import ReadableCourseDep

router = APIRouter(prefix="/tasks", tags=["tasks"])


@router.get(
    "/course/{course_id}/{note_id}/runs",
    response_model=list[ProcessingRunRead],
)
def list_processing_runs(
    course_id: UUID,
    note_id: UUID,
    session: SessionDep,
    _course: ReadableCourseDep,
) -> list[ProcessingRun]:
    try:
        return LectureProcessingService(session).list_runs(course_id, note_id)
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
    session: SessionDep,
    _course: ReadableCourseDep,
) -> ProcessingRun:
    try:
        return LectureProcessingService(session).get_run(course_id, note_id, run_id)
    except (
        LectureProcessingNoteNotFoundError,
        LectureProcessingRunNotFoundError,
    ) as exc:
        raise HTTPException(404, str(exc)) from exc

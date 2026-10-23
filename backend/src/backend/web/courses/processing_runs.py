from typing import Any
from uuid import UUID

from fastapi import HTTPException
from fastapi.routing import APIRouter

from backend.courses.exceptions import CourseNoteNotFoundError
from backend.processing.exceptions import (
    LectureAlreadyProcessedError,
    LectureProcessingRunNotFoundError,
)
from backend.processing.models import ProcessingRun
from backend.processing.schema import (
    LectureProcessingInput,
    LectureProcessingStatusRead,
    ProcessingRunRead,
)
from backend.processing.tasks import process_lecture_file

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
        LectureAlreadyProcessedError,
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


@router.post("/process")
async def start_lecture_processing(
    course_id: UUID,
    note_id: UUID,
    service: CourseNoteProcessingServiceDep,
    _note: ReadableCourseNoteDep,
) -> dict[str, Any]:
    try:
        await service.assert_can_process(note_id)
    except CourseNoteNotFoundError as exc:
        raise HTTPException(404, str(exc)) from exc
    except LectureAlreadyProcessedError as exc:
        raise HTTPException(409, str(exc)) from exc

    payload = LectureProcessingInput(course_id=course_id, note_id=note_id)
    task = process_lecture_file.apply_async(args=[payload.model_dump(mode="json")])  # type: ignore
    return {
        "course_id": course_id,
        "note_id": note_id,
        "task_id": task.id,
        "summary": "Processing lecture",
    }

from typing import Any
from uuid import UUID

from fastapi import HTTPException
from fastapi.routing import APIRouter
from starlette import status

from backend.courses.exceptions import CourseNoteNotFoundError
from backend.processing.exceptions import (
    LectureAlreadyProcessedError,
    LectureProcessingRunNotFoundError,
)
from backend.processing.models import (
    LectureProcessingInput,
    LectureProcessingStatusRead,
    ProcessingRun,
    ProcessingRunRead,
)
from backend.processing.tasks import process_lecture_file

from .dependencies import (
    CourseNoteProcessingServiceDep,
    OwnedCourseNoteDep,
    ReadableCourseNoteDep,
)

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
    note: OwnedCourseNoteDep,
) -> dict[str, Any]:

    # General checks to ensure we can process the note
    try:
        await service.assert_can_process(note_id)
        file = note.file
        if file is None or file.id is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Note does not have a file associated with it ",
            )
        if file.content_type != "application/pdf":
            raise HTTPException(
                status_code=status.HTTP_406_NOT_ACCEPTABLE,
                detail="Can only process pdf files ",
            )
    except CourseNoteNotFoundError as exc:
        raise HTTPException(404, str(exc)) from exc
    except LectureAlreadyProcessedError as exc:
        raise HTTPException(409, str(exc)) from exc

    payload = LectureProcessingInput(
        course_id=course_id, note_id=note_id, file_id=file.id
    )
    task = process_lecture_file.apply_async(args=[payload.model_dump(mode="json")])  # type: ignore
    return {
        "course_id": course_id,
        "note_id": note_id,
        "task_id": task.id,
        "summary": "Processing lecture",
    }

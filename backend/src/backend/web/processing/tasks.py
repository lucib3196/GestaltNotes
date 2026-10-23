from typing import Any
from uuid import UUID

from celery.result import AsyncResult
from fastapi import HTTPException
from fastapi.routing import APIRouter

from backend.courses.exceptions import CourseNoteNotFoundError
from backend.processing.celery_app import app
from backend.processing.exceptions import (
    LectureAlreadyProcessedError,
)
from backend.processing.schema import LectureProcessingInput
from backend.processing.tasks import process_lecture_file
from backend.web.courses.dependencies import ReadableCourseNoteDep

from .dependencies import CourseNoteProcessingServiceDep

router = APIRouter(prefix="/tasks", tags=["tasks"])


@router.get("/file/{task_id}")
def get_task_status(task_id: str) -> dict[str, Any]:
    task = AsyncResult(task_id, app=app)

    return {
        "task_id": task.id,
        "status": task.state,
        "result": task.result if task.successful() else None,
        "progress": task.info if task.state == "PROGRESS" else None,
        "error": str(task.result) if task.failed() else None,
    }


@router.post("/course/{course_id}/{note_id}")
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
    task = process_lecture_file.apply_async(args=[payload.model_dump(mode="json")])
    return {
        "course_id": course_id,
        "note_id": note_id,
        "task_id": task.id,
        "summary": "Processing lecture",
    }

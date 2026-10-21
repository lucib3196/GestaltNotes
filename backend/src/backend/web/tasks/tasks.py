from uuid import UUID

from celery.result import AsyncResult
from fastapi.routing import APIRouter

from backend.processing.celery_app import app
from backend.processing.tasks import process_lecture_file

ID = UUID | str

router = APIRouter(prefix="/tasks", tags=["tasks"])


@router.get("/file/{task_id}")
def get_task_status(task_id: str):
    task = AsyncResult(task_id, app=app) 


@router.post("/course/{course_id}/{note_id}/temp")
async def check(course_id: UUID, note_id: UUID):
    workflow = process_lecture_file.s(course_id, note_id)  # type: ignore
    task = workflow.apply_async()
    return {
        "course_id": course_id,
        "note_id": note_id,
        "task_id": task.id,
        "summary": "Processing lecture",
    }

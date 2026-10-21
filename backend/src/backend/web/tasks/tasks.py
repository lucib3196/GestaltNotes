from uuid import UUID

from celery.result import AsyncResult
from fastapi.routing import APIRouter

from backend.processing.celery_app import app
from backend.processing.schema import LectureTaskResponse, TaskProgress
from backend.processing.tasks import process_lecture_file

ID = UUID | str

router = APIRouter(prefix="/tasks", tags=["tasks"])


@router.get("/file/{task_id}", response_model=LectureTaskResponse)
def get_task_status(task_id: str):
    task = AsyncResult(task_id, app=app)
    return LectureTaskResponse(
        task_id=task_id,
        status=task.state,
        progress=(
            TaskProgress.model_validate(task.info) if task.state == "PROGRESS" else None
        ),
        result=task.result if task.successful() else None,
        error=str(task.result) if task.failed() else None,
    )


@router.post("/course/{course_id}/{note_id}/temp")
async def check(course_id: UUID, note_id: UUID):
    print("PROCESSING",note_id)
    workflow = process_lecture_file.s(course_id, note_id) # type: ignore
    task = workflow.apply_async()
    return {
        "course_id": course_id,
        "note_id": note_id,
        "task_id": task.id,
        "summary": "Processing lecture",
    }

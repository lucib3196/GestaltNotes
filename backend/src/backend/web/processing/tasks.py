from celery.result import AsyncResult
from fastapi.routing import APIRouter

from backend.processing.celery_app import app
from backend.processing.schema import TaskResponse, TaskState

router = APIRouter(prefix="/tasks", tags=["tasks"])


@router.get("/{task_id}", response_model=TaskResponse)
def get_task_status(task_id: str) -> TaskResponse:
    task = AsyncResult(task_id, app=app)
    return TaskResponse(
        task_id=task_id,
        status=TaskState(task.state),
        result=task.result if task.successful() else None,
        progress=task.info if task.state == TaskState.PROGRESS else None,
        error=str(task.result) if task.failed() else None,
    )

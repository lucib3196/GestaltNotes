from celery.result import AsyncResult
from fastapi.routing import APIRouter

from backend.processing.celery_app import app
from backend.processing.models import ProcessingStatus, TaskResponse

router = APIRouter(prefix="/tasks", tags=["tasks"])


@router.get("/{task_id}", response_model=TaskResponse)
def get_task_status(task_id: str) -> TaskResponse:
    """Inspect a single Celery task for debugging, not lecture-run progress."""
    task = AsyncResult(task_id, app=app)
    state = task.state
    return TaskResponse(
        task_id=task_id,
        status=ProcessingStatus(state),
        result=task.result if state == ProcessingStatus.SUCCESS else None,
        progress=task.info if state == ProcessingStatus.PROGRESS else None,
        error=str(task.result) if state == ProcessingStatus.FAILURE else None,
    )

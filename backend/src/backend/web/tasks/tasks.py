from uuid import UUID

from celery.result import AsyncResult
from fastapi.routing import APIRouter

from worker import app, random_number

ID = UUID | str

router = APIRouter(prefix="/tasks", tags=["tasks"])


@router.post("/")
def generate_number(number: int):
    task = random_number.delay(20)

    return {"status": "started", "id": task.id}


@router.get("/{task-id}")
def get_number(taks_id: str):
    result = AsyncResult(taks_id, app=app)
    if result.ready():
        return {"status": "complete", "value": result.get()}
    return {"status": "processing"}

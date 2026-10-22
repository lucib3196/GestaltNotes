from uuid import UUID

from pydantic import BaseModel, ConfigDict

from .model import ProcessingStage, ProcessingStatus


class ProcessingRunRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    celery_task_id: UUID
    task_type: str
    status: ProcessingStatus | None
    stage: ProcessingStage
    attempt_count: int
    error_type: str | None
    error_message: str | None

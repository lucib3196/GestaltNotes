from typing import Any, Literal
from uuid import UUID

from lecture_processor.graph.state import OutputState
from pydantic import BaseModel


class TaskProgress(BaseModel):
    stage: str
    message: str


class LectureTaskResponse(BaseModel):
    task_id: str
    status: Literal[
        "PENDING",
        "STARTED",
        "PROGRESS",
        "RETRY",
        "SUCCESS",
        "FAILURE",
        "REVOKED",
    ]
    progress: TaskProgress | None = None
    result: Any | None = None
    error: str | None = None


class ProcessedLecture(BaseModel):
    file_id: UUID | str
    file_name: str
    lecture: OutputState


class VectorizedLecture(ProcessedLecture):
    ids: list[str]

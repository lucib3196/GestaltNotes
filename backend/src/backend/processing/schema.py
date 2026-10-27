from enum import StrEnum
from uuid import UUID

from lecture_processor import OutputState
from pydantic import BaseModel, ConfigDict, Field, JsonValue, field_validator

from backend.courses.notes.models import NoteBlock

from .models import ProcessingStage, ProcessingStatus


class TaskState(StrEnum):
    PENDING = "PENDING"
    RECEIVED = "RECEIVED"
    STARTED = "STARTED"
    RETRY = "RETRY"
    FAILURE = "FAILURE"
    SUCCESS = "SUCCESS"
    REVOKED = "REVOKED"
    PROGRESS = "PROGRESS"


class TaskResponse(BaseModel):
    task_id: str
    status: TaskState
    result: JsonValue = None
    progress: JsonValue = None
    error: str | None = None


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


class LectureProcessingStatusRead(BaseModel):
    has_succeeded: bool
    can_process: bool
    latest_run: ProcessingRunRead | None


class LectureProcessingInput(BaseModel):
    course_id: UUID
    note_id: UUID


class LectureProcessingState(LectureProcessingInput):
    run_id: UUID
    file_id: UUID
    extraction_result: OutputState | None = None
    note_blocks: list[NoteBlock] = Field(default_factory=list)
    vector_ids: list[str] = Field(default_factory=list)

    @field_validator("note_blocks", mode="before")
    @classmethod
    def validate_note_blocks(cls, blocks: object) -> object:
        # SQLModel table constructors do not fully validate broker JSON.
        if isinstance(blocks, list):
            return [
                NoteBlock.model_validate(block) if isinstance(block, dict) else block
                for block in blocks
            ]
        return blocks


class RunUpdate(BaseModel):
    celery_task_id: UUID | None = None
    task_type: str | None = None
    status: ProcessingStatus | None = None
    stage: ProcessingStage | None = None
    attempt_count: int | None = Field(default=None, ge=0)
    error_type: str | None = None
    error_message: str | None = None

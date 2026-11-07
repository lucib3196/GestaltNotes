from datetime import UTC, datetime
from enum import StrEnum
from typing import TYPE_CHECKING, Optional
from uuid import UUID, uuid4

from lecture_processor import OutputState
from pydantic import BaseModel, ConfigDict, JsonValue, field_validator
from sqlalchemy import Column, DateTime, ForeignKey
from sqlalchemy import Enum as SAEnum
from sqlmodel import Field, Relationship, SQLModel

from backend.courses.models import NoteBlock

if TYPE_CHECKING:
    from backend.courses.models import CourseNote, NoteBlock


# ---------------------------------------------------------------------------
# Status and stage enums
# ---------------------------------------------------------------------------


class ProcessingStatus(StrEnum):
    PENDING = "PENDING"
    RECEIVED = "RECEIVED"
    STARTED = "STARTED"
    RETRY = "RETRY"
    FAILURE = "FAILURE"
    SUCCESS = "SUCCESS"
    REVOKED = "REVOKED"
    PROGRESS = "PROGRESS"


class ProcessingStage(StrEnum):
    VALIDATING = "validating"
    DOWNLOADING = "downloading"
    EXTRACTING = "extracting"
    SAVING_BLOCKS = "saving_blocks"
    BUILDING_DOCUMENTS = "building_documents"
    INDEXING = "indexing"


# ---------------------------------------------------------------------------
# Shared processing-run fields
# ---------------------------------------------------------------------------


class ProcessingRunBase(SQLModel):
    celery_task_id: UUID
    task_type: str
    status: ProcessingStatus
    stage: ProcessingStage
    attempt_count: int = Field(default=0, ge=0)
    error_type: str | None = None
    error_message: str | None = None


# ---------------------------------------------------------------------------
# Database tables and relationships
# ---------------------------------------------------------------------------


class ProcessingRun(ProcessingRunBase, table=True):
    __tablename__ = "processing_run"  # type: ignore
    id: UUID = Field(default_factory=uuid4, primary_key=True)
    status: ProcessingStatus = Field(
        default=ProcessingStatus.PENDING,
        sa_column=Column(
            SAEnum(ProcessingStatus, name="processing_status"),
            nullable=False,
        ),
    )
    stage: ProcessingStage = Field(
        sa_column=Column(
            SAEnum(
                ProcessingStage,
                name="processing_stage",
            ),
            nullable=False,
        ),
    )
    created_at: datetime = Field(
        default_factory=lambda: datetime.now(UTC),
        sa_column=Column(DateTime(timezone=True), nullable=False),
    )
    updated_at: datetime = Field(
        default_factory=lambda: datetime.now(UTC),
        sa_column=Column(
            DateTime(timezone=True),
            nullable=False,
            onupdate=lambda: datetime.now(UTC),
        ),
    )

    lecture_run: Optional["LectureProcessingRun"] = Relationship(
        back_populates="run",
        sa_relationship_kwargs={"uselist": False},
    )


class LectureProcessingRun(SQLModel, table=True):
    __tablename__ = "lecture_processing_run"  # type: ignore

    run_id: UUID = Field(
        sa_column=Column(
            ForeignKey("processing_run.id", ondelete="CASCADE"),
            nullable=False,
            primary_key=True,
        )
    )
    note_id: UUID = Field(
        sa_column=Column(
            ForeignKey("course_note.id", ondelete="CASCADE"),
            nullable=False,
            index=True,
        )
    )

    run: "ProcessingRun" = Relationship(
        back_populates="lecture_run",
        sa_relationship_kwargs={"lazy": "selectin"},
    )
    note: "CourseNote" = Relationship(
        back_populates="processing_runs",
        sa_relationship_kwargs={"lazy": "selectin"},
    )


# ---------------------------------------------------------------------------
# Read and update schemas
# ---------------------------------------------------------------------------


class ProcessingRunRead(ProcessingRunBase):
    """Public representation of a persisted processing run."""

    id: UUID
    created_at: datetime
    updated_at: datetime


class ProcessingUpdate(BaseModel):
    model_config = ConfigDict(extra="forbid")

    celery_task_id: UUID | None = None
    task_type: str | None = None
    status: ProcessingStatus | None = None
    stage: ProcessingStage | None = None
    attempt_count: int | None = Field(default=None, ge=0)
    error_type: str | None = None
    error_message: str | None = None


# ---------------------------------------------------------------------------
# Celery task inputs and intermediate state
# ---------------------------------------------------------------------------


class LectureProcessingInput(BaseModel):
    course_id: UUID
    note_id: UUID
    file_id: UUID


class LectureProcessingState(LectureProcessingInput):
    run_id: UUID
    extraction_result: OutputState | None = None
    note_blocks: list[NoteBlock] = Field(default_factory=list)

    @field_validator("note_blocks", mode="before")
    @classmethod
    def validate_note_blocks(cls, blocks: object) -> object:
        # SQLModel table constructors do not fully validate broker JSON.
        if isinstance(blocks, list):
            from backend.courses.models import NoteBlock

            return [
                NoteBlock.model_validate(block) if isinstance(block, dict) else block
                for block in blocks
            ]
        return blocks


# ---------------------------------------------------------------------------
# API responses
# ---------------------------------------------------------------------------


class TaskResponse(BaseModel):
    task_id: str
    status: ProcessingStatus
    result: JsonValue = None
    progress: JsonValue = None
    error: str | None = None


class LectureProcessingStatusRead(BaseModel):
    has_succeeded: bool
    can_process: bool
    latest_run: ProcessingRunRead | None


# ---------------------------------------------------------------------------
# Resolve cross-module model references
# ---------------------------------------------------------------------------

# Resolve task payload references after all processing models are defined.
# Course models import LectureProcessingStatusRead from this module.
from backend.courses.models import NoteBlock  # noqa: E402

LectureProcessingState.model_rebuild(_types_namespace={"NoteBlock": NoteBlock})

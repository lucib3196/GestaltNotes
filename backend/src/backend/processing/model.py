from enum import StrEnum
from typing import TYPE_CHECKING, Optional
from uuid import UUID, uuid4

from sqlalchemy import Column, ForeignKey
from sqlalchemy import Enum as SAEnum
from sqlmodel import Field, Relationship, SQLModel

if TYPE_CHECKING:
    from backend.courses.models import CourseNote


class ProcessingStatus(StrEnum):
    QUEUED = "queued"
    RUNNING = "running"
    RETRYING = "retrying"
    SUCCEEDED = "succeeded"
    PARTIAL = "partial"
    FAILED = "failed"
    REVOKED = "revoked"


class ProcessingStage(StrEnum):
    DOWNLOADING = "downloading"
    EXTRACTING = "extracting"
    SAVING_BLOCKS = "saving_blocks"
    BUILDING_DOCUMENTS = "building_documents"
    INDEXING = "indexing"


class ProcessingRun(SQLModel, table=True):
    __tablename__ = "processing_run"  # type: ignore
    id: UUID | None = Field(default_factory=uuid4, primary_key=True)
    celery_task_id: UUID
    task_type: str
    status: ProcessingStatus | None = Field(
        sa_column=Column(
            SAEnum(
                ProcessingStatus,
                name="processing_status",
            ),
            nullable=True,
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
    attempt_count: int = 0
    error_type: str | None = None
    error_message: str | None = None

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

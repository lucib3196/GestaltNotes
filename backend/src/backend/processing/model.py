from enum import StrEnum
from uuid import UUID, uuid4
from sqlalchemy import Column, ForeignKey
from sqlmodel import Field, SQLModel
from sqlmodel import Field, Relationship, SQLModel
from sqlalchemy import Column, Enum as SAEnum
from typing import Optional, TYPE_CHECKING

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


class FileProcessing(SQLModel, table=True):
    __tablename__ = "file_processing"  # type: ignore
    id: UUID | None = Field(default_factory=uuid4, primary_key=True)
    celery_task_id: UUID
    task_type: str
    status: ProcessingStatus = Field(
    sa_column=Column(
        SAEnum(
            ProcessingStatus,
            name="processing_status",
        ),
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
    attempt_count: int
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
            ForeignKey("file_processing.id", ondelete="CASCADE"),
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

    run: "FileProcessing" = Relationship(
        back_populates="lecture_run",
        sa_relationship_kwargs={"lazy": "selectin"},
    )
    note: "CourseNote" = Relationship(
        back_populates="processing_runs",
        sa_relationship_kwargs={"lazy": "selectin"},
    )
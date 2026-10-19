from datetime import datetime
from enum import StrEnum
from typing import Any
from uuid import UUID, uuid4

from sqlalchemy import JSON, Column, Enum, ForeignKey
from sqlalchemy.dialects.postgresql import JSONB
from sqlmodel import Field, SQLModel

JSONType = JSON().with_variant(JSONB, "postgresql")


class File(SQLModel, table=True):
    id: UUID | None = Field(default_factory=uuid4, primary_key=True)
    parent_id: UUID | None = Field(
        default=None,
        sa_column=Column(ForeignKey("file.id", ondelete="CASCADE"), nullable=True),
    )
    owner_id: UUID = Field(foreign_key="user.id", index=True)
    original_name: str
    storage_key: str = Field(description="Points to storage location")
    content_type: str | None = None
    size_bytes: int | None = None
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)


class ProcessingStatus(StrEnum):
    QUEUED = "queued"
    RUNNING = "running"
    RETRYING = "retrying"
    SUCCEEDED = "succeeded"
    FAILED = "failed"
    REVOKED = "revoked"


class FileProcessing(SQLModel, table=True):
    __tablename__ = "file_processing"  # type: ignore
    id: UUID | None = Field(default_factory=uuid4, primary_key=True)
    file_id: UUID | None = Field(
        sa_column=Column(ForeignKey("file.id", ondelete="CASCADE"), nullable=False)
    )
    celery_task_id: UUID
    status: ProcessingStatus = Field(
        sa_column=Column(
            Enum(ProcessingStatus, name="processing_status"),
            nullable=False,
        )
    )
    stage: str | None = None
    started_at: datetime = Field(default_factory=datetime.utcnow)
    finished_at: datetime | None = None
    error_message: str | None = None


class Document(SQLModel, table=True):
    id: UUID = Field(default_factory=uuid4, primary_key=True)
    source_file_id: UUID = Field(foreign_key="file.id")
    title: str
    content: dict[str, Any] = Field(
        default_factory=dict,
        sa_column=Column(JSONType, nullable=False),
    )
    kind: str | None = None
    version: int = 1

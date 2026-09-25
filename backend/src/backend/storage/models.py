from sqlmodel import SQLModel, Field
from uuid import uuid4, UUID
from enum import StrEnum
from dataclasses import dataclass
from datetime import datetime


class File(SQLModel, table=True):
    id: UUID | None = Field(default_factory=uuid4)
    owner_id: UUID = Field(foreign_key="user.id", primary_key=True)
    original_name: str
    storage_key: str = Field(description="Points to storage location")
    content_type: str | None = None
    size_bytes: int | None = None
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)


@dataclass
class BlobMetadata:
    key: str
    size: int|None
    content_type: str | None
    created_at: datetime | None = None
    updated_at: datetime | None = None
    checksum: str | None = None

from datetime import datetime
from uuid import UUID, uuid4

from pydantic import BaseModel
from pydantic import Field as PydanticField
from sqlmodel import Field, SQLModel


class File(SQLModel, table=True):
    id: UUID | None = Field(default_factory=uuid4,primary_key=True)
    owner_id: UUID = Field(foreign_key="user.id", index=True)
    original_name: str
    storage_key: str = Field(description="Points to storage location")
    content_type: str | None = None
    size_bytes: int | None = None
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)


class FileUpdate(BaseModel):
    content_type: str | None = None
    size_bytes: int | None = PydanticField(default=None, ge=0)

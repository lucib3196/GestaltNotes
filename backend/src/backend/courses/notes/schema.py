from datetime import datetime
from typing import Any
from uuid import UUID

from pydantic import BaseModel, ConfigDict


class NoteBlockRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    course_id: UUID | None
    source_file_id: UUID | None
    title: str
    kind: str | None
    content: dict[str, Any]
    position: int
    page_start: int | None
    page_end: int | None
    revision: int
    schema_version: int
    created_at: datetime
    updated_at: datetime

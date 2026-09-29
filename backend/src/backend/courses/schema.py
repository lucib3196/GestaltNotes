from uuid import UUID

from pydantic import BaseModel, Field
from .models import CourseContentType

class CourseCreate(BaseModel):
    name: str = Field(min_length=1)
    discipline: str | None = None
    description: str | None = None


class CourseUpdate(BaseModel):
    name: str | None = Field(default=None, min_length=1)
    discipline: str | None = None
    description: str | None = None


class CourseRead(BaseModel):
    id: UUID
    name: str
    discipline: str | None = None
    description: str | None = None
    owner_id: UUID
    storage_prefix: str | None = None


class CourseDelete(BaseModel):
    success: bool
    info: str


class CourseNoteUpdate(BaseModel):
    title: str | None = None
    resource_type: CourseContentType | None = None
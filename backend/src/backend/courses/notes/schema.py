from datetime import datetime
from typing import Any
from uuid import UUID

from pydantic import BaseModel, ConfigDict

from backend.processing.schema import LectureProcessingStatusRead

from .models import CourseContentType


class CourseNoteRead(BaseModel):
    id: UUID
    course_id: UUID
    file_id: UUID
    title: str
    resource_type: CourseContentType
    download_url: str | None = None
    content_type: str | None = None


class CourseNoteDelete(BaseModel):
    success: bool
    info: str


class CourseNoteUpdate(BaseModel):
    title: str | None = None
    resource_type: CourseContentType | None = None


class NoteOverview(CourseNoteRead):
    processing: LectureProcessingStatusRead


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

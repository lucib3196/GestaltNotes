from datetime import datetime
from enum import StrEnum
from typing import TYPE_CHECKING, Any, Optional
from uuid import UUID, uuid4

from lecture_processor.conceptual_question import ConceptualQuestion
from lecture_processor.extract_derivations.model import Derivation
from lecture_processor.extracted_question import ExtractedQuestion
from lecture_processor.lecture_analysis import LectureAnalysis
from pydantic import BaseModel
from sqlalchemy import JSON, Column, ForeignKey, UniqueConstraint
from sqlalchemy import Enum as SAEnum
from sqlalchemy.dialects.postgresql import JSONB
from sqlmodel import Field, Relationship, SQLModel

from backend.shared import Status

if TYPE_CHECKING:
    from backend.courses.models import Course
    from backend.processing.models import LectureProcessingRun
    from backend.storage.models import File
JSONType = JSON().with_variant(JSONB, "postgresql")

NOTE_BLOCK_CONTENT_MODELS: dict[str, type[BaseModel]] = {
    "lecture_summary": LectureAnalysis,
    "conceptual_question": ConceptualQuestion,
    "derivation": Derivation,
    "extracted_question": ExtractedQuestion,
}


class CourseContentType(StrEnum):
    LECTURE = "lecture"
    NOTES = "notes"
    ASSIGNMENT = "assignment"
    EXAM = "exam"
    QUIZ = "quiz"
    TEXTBOOK = "textbook"
    HANDOUT = "handout"
    SYLLABUS = "syllabus"
    REFERENCE = "reference"
    OTHER = "other"


class CourseNote(SQLModel, table=True):
    __tablename__ = "course_note"  # type: ignore
    __table_args__ = (
        UniqueConstraint("course_id", "file_id", name="uq_course_note_course_file"),
    )

    id: UUID | None = Field(default_factory=uuid4, primary_key=True)
    course_id: UUID = Field(
        sa_column=Column(ForeignKey("course.id", ondelete="CASCADE"), nullable=False)
    )
    file_id: UUID = Field(
        sa_column=Column(ForeignKey("file.id", ondelete="CASCADE"), nullable=False)
    )
    title: str
    resource_type: CourseContentType = Field(
        sa_column=Column(
            SAEnum(CourseContentType, name="course_content_type"),
            nullable=False,
        )
    )
    status: Status = Status.DRAFT

    course: "Course" = Relationship(back_populates="notes")

    file: "File" = Relationship(sa_relationship_kwargs={"lazy": "selectin"})

    processing_runs: list["LectureProcessingRun"] = Relationship(
        back_populates="note",
    )


class NoteBlock(SQLModel, table=True):
    __tablename__ = "note_block"  # type: ignore

    # Identity and source
    id: UUID = Field(
        default_factory=uuid4,
        primary_key=True,
        description="Unique identifier for this editable note block.",
    )
    course_id: UUID | None = Field(
        default=None,
        sa_column=Column(
            ForeignKey("course.id", ondelete="CASCADE"),
            nullable=True,
            index=True,
        ),
        description="The course in which this block lives in",
    )
    source_file_id: UUID | None = Field(
        default=None,
        sa_column=Column(
            ForeignKey("file.id", ondelete="CASCADE"),
            nullable=True,
            index=True,
        ),
        description=(
            "Source file from which this block was extracted. "
            "Deleting the source file also deletes its blocks."
        ),
    )
    course: Optional["Course"] = Relationship(
        sa_relationship_kwargs={"lazy": "selectin"}
    )
    file: Optional["File"] = Relationship(sa_relationship_kwargs={"lazy": "selectin"})

    # Editable content
    title: str = Field(
        description="Display title for this block.",
    )
    kind: str | None = Field(
        default=None,
        description=(
            "Content category, such as derivation, extracted_question, "
            "conceptual_question, or lecture_summary."
        ),
    )
    content: dict[str, Any] = Field(
        default_factory=dict,
        sa_column=Column(JSONType, nullable=False),
        description="Structured JSON payload containing the editable block content.",
    )

    # Ordering and source location
    position: int = Field(
        ge=0,
        description="Zero-based display position within the source file's blocks.",
    )
    page_start: int | None = Field(
        default=None,
        ge=0,
        description="Zero-based first source PDF page, inclusive, if known.",
    )
    page_end: int | None = Field(
        default=None,
        ge=0,
        description="Zero-based last source PDF page, inclusive, if known.",
    )

    # Versioning
    revision: int = Field(
        default=0,
        ge=0,
        description=(
            "Content revision, starting at zero. "
            "Increment when editable content changes."
        ),
    )
    schema_version: int = Field(
        default=1,
        ge=1,
        description=(
            "Version of the JSON content structure, used to interpret "
            "and migrate stored payloads."
        ),
    )

    # Timestamps
    created_at: datetime = Field(
        default_factory=datetime.utcnow,
        description="UTC creation time.",
    )
    updated_at: datetime = Field(
        default_factory=datetime.utcnow,
        description=(
            "UTC time of the last update. "
            "The update service must refresh this value when saving changes."
        ),
    )

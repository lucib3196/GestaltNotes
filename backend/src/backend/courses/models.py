from datetime import datetime
from enum import StrEnum
from typing import TYPE_CHECKING, Any, Optional
from uuid import UUID, uuid4

from lecture_processor.conceptual_question import ConceptualQuestion
from lecture_processor.extract_derivations.model import Derivation
from lecture_processor.extracted_question import ExtractedQuestion
from lecture_processor.lecture_analysis import LectureAnalysis
from pydantic import BaseModel, ConfigDict
from sqlalchemy import JSON, Column, DateTime, ForeignKey, Index, UniqueConstraint
from sqlalchemy import Enum as SAEnum
from sqlalchemy.dialects.postgresql import JSONB
from sqlmodel import Field, Relationship, SQLModel

from backend.shared import Status

if TYPE_CHECKING:
    from backend.accounts.models import User
    from backend.processing.models import LectureProcessingRun
    from backend.storage.models import File

JSONType = JSON().with_variant(JSONB, "postgresql")


# --------------------------------------------------------------------
# ---------------- Courses and Enrollments ----------------
# --------------------------------------------------------------------


class CourseEnrollmentBase(SQLModel):
    student_id: UUID
    course_id: UUID


class CourseEnrollmentCreate(CourseEnrollmentBase):
    pass


class CourseEnrollmentRead(CourseEnrollmentBase):
    enrolled_at: datetime
    active: bool


class CourseEnrollmentUpdate(CourseEnrollmentBase):
    active: bool


class CourseEnrollment(CourseEnrollmentBase, table=True):
    __tablename__ = "course_enrollment"  # type: ignore
    # Ensures that a student can only be enrolled in a course once
    __table_args__ = (
        UniqueConstraint(
            "student_id", "course_id", name="uq_course_enrollment_student_id"
        ),
    )

    student_id: UUID = Field(foreign_key="user.id", primary_key=True)
    course_id: UUID = Field(foreign_key="course.id", primary_key=True)

    enrolled_at: datetime = Field(default_factory=datetime.utcnow)
    active: bool = True


class CourseBase(SQLModel):
    name: str
    discipline: str | None = None
    description: str | None = None


class CourseCreate(CourseBase):
    pass


class CourseUpdate(CourseBase):
    pass


class CourseRead(CourseBase):
    id: UUID
    owner_id: UUID


class Course(CourseBase, table=True):
    id: UUID = Field(default_factory=uuid4, primary_key=True)
    owner_id: UUID = Field(
        sa_column=Column(ForeignKey("user.id", ondelete="CASCADE"), nullable=False)
    )
    prompt: str | None = None
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

    # Attributes
    owner: "User" = Relationship(back_populates="owned_courses")
    students: list["User"] = Relationship(
        back_populates="enrolled_courses",
        link_model=CourseEnrollment,
    )

    notes: list["CourseNote"] = Relationship(back_populates="course")
    vectorstore: Optional["CourseVectorStore"] = Relationship(back_populates="course")

    @property
    def storage_prefix(self) -> str:
        return f"courses/{self.id}"


class CourseModuleBase(SQLModel):
    course_id: UUID = Field()
    title: str
    position: int = Field(default=0)


class CourseModule(CourseModuleBase, table=True):
    __tablename__ = "course_module"  # type: ignore

    __table_args__ = (
        UniqueConstraint("course_id", "id", name="uq_course_module_course_id"),
        Index("ix_course_modules_course_position", "course_id", "position"),
    )

    id: UUID | None = Field(default_factory=uuid4, primary_key=True)

    course_id: UUID = Field(
        sa_column=Column(ForeignKey("course.id", ondelete="CASCADE"), nullable=False)
    )

    created_at: datetime = Field(default_factory=datetime.utcnow)

    updated_at: datetime = Field(
        default_factory=datetime.utcnow,
        sa_column=Column(
            DateTime(timezone=True),
            nullable=False,
            default=datetime.utcnow,
            onupdate=datetime.utcnow,
        ),
    )


# --------------------------------------------------------------------
# ---------------- Course Notes and Note Blocks ----------------
# --------------------------------------------------------------------

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


class CourseNoteBase(SQLModel):
    course_id: UUID = Field()
    file_id: UUID = Field()
    title: str
    resource_type: CourseContentType = Field()


class CourseNote(CourseNoteBase, table=True):
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


class NoteBlockBase(SQLModel):
    course_id: UUID | None = Field(
        default=None, description="The course in which this block lives in"
    )
    source_file_id: UUID | None = Field(
        default=None,
        description=(
            "Source file from which this block was extracted. Deleting the "
            "source file also deletes its blocks."
        ),
    )
    title: str = Field(description="Display title for this block.")
    kind: str | None = Field(
        default=None,
        description=(
            "Content category, such as derivation, extracted_question, "
            "conceptual_question, or lecture_summary."
        ),
    )
    content: dict[str, Any] = Field(
        default_factory=dict,
        description="Structured JSON payload containing the editable block content.",
    )
    position: int = Field(
        ge=0, description="Zero-based display position within the source file's blocks."
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
    revision: int = Field(
        default=0,
        ge=0,
        description=(
            "Content revision, starting at zero. Increment when editable "
            "content changes."
        ),
    )
    schema_version: int = Field(
        default=1,
        ge=1,
        description=(
            "Version of the JSON content structure, used to interpret and "
            "migrate stored payloads."
        ),
    )


class NoteBlock(NoteBlockBase, table=True):
    __tablename__ = "note_block"  # type: ignore

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

    content: dict[str, Any] = Field(
        default_factory=dict,
        sa_column=Column(JSONType, nullable=False),
        description="Structured JSON payload containing the editable block content.",
    )

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


# --------------------------------------------------------------------
# ---------------- Course Note Schemas ----------------
# --------------------------------------------------------------------


class CourseNoteRead(CourseNoteBase):
    id: UUID
    download_url: str | None = None
    content_type: str | None = None


class DeleteResponseBase(BaseModel):
    success: bool
    info: str


class CourseNoteDelete(DeleteResponseBase):
    pass


class CourseNoteUpdate(BaseModel):
    title: str | None = None
    resource_type: CourseContentType | None = None


class NoteBlockRead(NoteBlockBase):
    model_config = ConfigDict(from_attributes=True)  # type: ignore

    id: UUID
    created_at: datetime
    updated_at: datetime


# --------------------------------------------------------------------
# ---------------- Course Response Schemas ----------------
# --------------------------------------------------------------------


class CourseDelete(DeleteResponseBase):
    pass


# --------------------------------------------------------------------
# ---------------- Course Vector Stores ----------------
# --------------------------------------------------------------------


class VectorStoreStatus(StrEnum):
    PENDING = "pending"
    READY = "ready"
    FAILED = "failed"
    ARCHIVED = "archieved"


class VectorstoreProvider(StrEnum):
    ASTRA = "astra"
    POSTGRES = "postgres"


class CourseVectorStoreBase(SQLModel):
    course_id: UUID = Field()
    namespace_key: str = Field()
    collection_name: str = Field()
    description: str | None = Field(default=None)
    embedding_model: str
    provider: VectorstoreProvider = Field()
    status: VectorStoreStatus = Field()


class CourseVectorStore(CourseVectorStoreBase, table=True):
    __tablename__ = "course_vector_store"  # type: ignore

    course_id: UUID = Field(
        sa_column=Column(
            ForeignKey("course.id", ondelete="CASCADE"),
            nullable=False,
            primary_key=True,
        )
    )

    namespace_key: str = Field(unique=True, nullable=False)

    collection_name: str = Field(nullable=False)

    provider: VectorstoreProvider = Field(
        sa_column=Column(
            SAEnum(VectorstoreProvider, name="vector_store_provider"),
            nullable=False,
        ),
    )

    status: VectorStoreStatus = Field(
        sa_column=Column(
            SAEnum(VectorStoreStatus, name="vector_store_status"),
            nullable=False,
        ),
    )

    course: "Course" = Relationship(back_populates="vectorstore")


# --------------------------------------------------------------------
# ---------------- Note Processing Overview --------------------------
# --------------------------------------------------------------------

# NoteBlock must be defined before importing the processing schemas.
from backend.processing.schema import LectureProcessingStatusRead  # noqa: E402


class NoteOverview(CourseNoteRead):
    processing: LectureProcessingStatusRead

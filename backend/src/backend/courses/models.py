from datetime import datetime
from enum import StrEnum
from typing import TYPE_CHECKING
from uuid import UUID, uuid4
from backend.shared import Status
from sqlalchemy import Column, ForeignKey, UniqueConstraint, Index
from sqlmodel import Field, Relationship, SQLModel
from sqlalchemy import Column, DateTime, ForeignKey, Index, UniqueConstraint
if TYPE_CHECKING:
    from backend.accounts.models import User
    from backend.storage.repo.schema import File


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


class CourseEnrollment(SQLModel, table=True):
    __tablename__ = "course_enrollment"  # type: ignore
    __table_args__ = (
        UniqueConstraint(
            "student_id", "course_id", name="uq_course_enrollment_student_id"
        ),
    )

    student_id: UUID = Field(foreign_key="user.id", primary_key=True)
    course_id: UUID = Field(foreign_key="course.id", primary_key=True)

    enrolled_at: datetime = Field(default_factory=datetime.utcnow)
    active: bool = True


class Course(SQLModel, table=True):
    id: UUID | None = Field(default_factory=uuid4, primary_key=True)
    name: str
    discipline: str | None
    description: str | None = None

    owner_id: UUID = Field(
        sa_column=Column(ForeignKey("user.id", ondelete="CASCADE"), nullable=False)
    )
    owner: "User" = Relationship(back_populates="owned_courses")
    students: list["User"] = Relationship(
        back_populates="enrolled_courses",
        link_model=CourseEnrollment,
    )

    notes: list["CourseNote"] = Relationship(back_populates="course")
    access_codes: list["CourseAccessCode"] = Relationship(back_populates="course")

    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

    @property
    def storage_prefix(self) -> str:
        return f"courses/{self.id}"


class CourseAccessCode(SQLModel, table=True):
    __tablename__ = "course_access_code"  # type: ignore
    id: UUID | None = Field(default_factory=uuid4, primary_key=True)
    course_id: UUID = Field(
        sa_column=Column(ForeignKey("course.id", ondelete="CASCADE"), nullable=False)
    )
    code_hash: str = Field(unique=True, index=True)
    active: bool = True
    created_at: datetime = Field(default_factory=datetime.utcnow)
    expires_at: datetime | None = None
    uses: int = 0

    course: "Course" = Relationship(back_populates="access_codes")


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
    resource_type: CourseContentType
    status: Status = Status.DRAFT

    course: "Course" = Relationship(back_populates="notes")

    file: "File" = Relationship(sa_relationship_kwargs={"lazy": "selectin"})


class CourseModule(SQLModel, table=True):
    __tablename__ = "course_module"  # type: ignore
    __table_args__ = (
        UniqueConstraint("course_id", "id", name="uq_course_module_course_id"),
        Index("ix_course_modules_course_position", "course_id", "position"),
    )
    id: UUID | None = Field(default_factory=uuid4, primary_key=True)
    course_id: UUID = Field(
        sa_column=Column(ForeignKey("course.id", ondelete="CASCADE"), nullable=False)
    )
    title: str
    position: int = Field(default=0)
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

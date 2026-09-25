from datetime import datetime
from typing import TYPE_CHECKING
from uuid import UUID, uuid4

from sqlalchemy import Column, ForeignKey, UniqueConstraint
from sqlmodel import Field, Relationship, SQLModel

if TYPE_CHECKING:
    from backend.accounts.models import User


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

    storage_prefix: str | None = Field(
        default=None,
        description="Cloud storage folder/prefix for course assets",
    )
    lecture_notes: list["LectureNote"] = Relationship(back_populates="course")
    access_codes: list["CourseAccessCode"] = Relationship(back_populates="course")

    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)


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


class LectureNote(SQLModel, table=True):
    __tablename__ = "lecture_note"  # type: ignore
    id: UUID | None = Field(default_factory=uuid4, primary_key=True)
    course_id: UUID = Field(
        sa_column=Column(ForeignKey("course.id", ondelete="CASCADE"), nullable=False)
    )
    title: str
    original_filename: str
    storage_path: str = Field(unique=True)

    # File data
    content_type: str | None = None
    file_size_bytes: int | None = None

    uploaded_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

    course: "Course" = Relationship(back_populates="lecture_notes")

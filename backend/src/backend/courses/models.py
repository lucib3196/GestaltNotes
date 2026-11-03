from datetime import datetime
from typing import TYPE_CHECKING, Optional
from uuid import UUID, uuid4

from sqlalchemy import Column, DateTime, ForeignKey, Index, UniqueConstraint
from sqlmodel import Field, Relationship, SQLModel

from backend.courses.notes.models import CourseContentType as CourseContentType
from backend.courses.notes.models import CourseNote as CourseNote
from backend.courses.vector_store.models import (
    CourseVectorStore as CourseVectorStore,
)
from backend.courses.vector_store.models import (
    VectorStoreStatus as VectorStoreStatus,
)

if TYPE_CHECKING:
    from backend.accounts.models import User
    from backend.courses.vector_store.models import CourseVectorStore


# --------------------------------------------------------------------
# ------------------- Course Enrollments -----------------------------
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


# ------------------------------------
# ------------ Course Models ---------
# ------------------------------------
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
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

    # Attributes
    owner: "User" = Relationship(back_populates="owned_courses")
    students: list["User"] = Relationship(
        back_populates="enrolled_courses",
        link_model=CourseEnrollment,
    )

    notes: list["CourseNote"] = Relationship(back_populates="course")
    access_codes: list["CourseAccessCode"] = Relationship(back_populates="course")
    vectorstore: Optional["CourseVectorStore"] = Relationship(back_populates="course")

    @property
    def storage_prefix(self) -> str:
        return f"courses/{self.id}"


# -------------------------------------------------------------------
# ---------------- Extra TBD-----------------------------------------
# -------------------------------------------------------------------
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

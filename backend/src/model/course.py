from sqlmodel import SQLModel, Field, Relationship
from typing import List, Optional, TYPE_CHECKING
from uuid import uuid4, UUID
from pydantic import BaseModel
from .user import UserCourseLink
from datetime import datetime

if TYPE_CHECKING:
    from .user import User, Thread


class Course(SQLModel, table=True):
    id: Optional[UUID] = Field(default_factory=uuid4, primary_key=True)
    name: str
    discipline: str
    blob: str | None = Field(
        default=None, description="Location to store data for cloud storage"
    )
    description: str | None = Field(default=None)

    owner: UUID | None = Field(default=None, foreign_key="user.id")

    threads: List["Thread"] = Relationship(back_populates="course")
    
    educators: list["User"] = Relationship(
        back_populates="courses",
        link_model=UserCourseLink,
    )

    lecture_notes: list["LectureNote"] = Relationship()


class CourseData(BaseModel):
    name: str
    discipline: str
    blob: str | None
    description: str | None


class StudentCourseLink(SQLModel, table=True):
    student_id: UUID | None = Field(
        default=None, foreign_key="user.id", primary_key=True
    )
    course_id: UUID | None = Field(
        default=None, foreign_key="course.id", primary_key=True
    )

class LectureNote(SQLModel, table=True):
    id: Optional[UUID] = Field(default_factory=uuid4, primary_key=True)
    course_id: UUID = Field(foreign_key="course.id")
    title: str
    file_name: str
    file_url: str
    uploaded_at: datetime = Field(default_factory=datetime.utcnow)
    
class LectureNoteCreate(BaseModel):
    title: str
    file_name: str
    file_url: str

from datetime import datetime
from typing import Optional, TYPE_CHECKING, List
from uuid import UUID, uuid4

from sqlmodel import SQLModel, Field, Relationship

if TYPE_CHECKING:
    from .user import User
    from .course import Course


class Thread(SQLModel, table=True):
    id: Optional[UUID] = Field(default_factory=uuid4, primary_key=True)

    user_id: UUID = Field(foreign_key="user.id")
    course_id: Optional[UUID] = Field(default=None, foreign_key="course.id")

    title: Optional[str] = None
    agent: Optional[str] = None

    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

    user: "User" = Relationship(back_populates="threads")
    course: "Course" = Relationship(back_populates="threads")
    messages: List["Message"] = Relationship(back_populates="thread")


class Message(SQLModel, table=True):
    id: Optional[UUID] = Field(default_factory=uuid4, primary_key=True)

    thread_id: UUID = Field(foreign_key="thread.id")
    role: str
    content: str
    created_at: datetime = Field(default_factory=datetime.utcnow)

    thread: "Thread" = Relationship(back_populates="messages")
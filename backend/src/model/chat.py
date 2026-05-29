from datetime import datetime
from typing import TYPE_CHECKING
from uuid import UUID, uuid4

from pydantic import BaseModel
from sqlmodel import Field, Relationship, SQLModel

if TYPE_CHECKING:
    from .course import Course
    from .user import User
    


class ThreadCreate(BaseModel):
    thread_id: UUID | str | None = None
    user_id: UUID | str | None = None
    course_id: UUID | str | None = None
    title: str | None = None
    agent: str | None = None


class ThreadUpdate(BaseModel):
    title: str | None = None


class ThreadList(BaseModel):
    user_id: UUID
    course_id: UUID | None = None


class MessageCreate(BaseModel):
    role: str
    content: str


class Thread(SQLModel, table=True):
    id: UUID | None = Field(default_factory=uuid4, primary_key=True)

    user_id: UUID = Field(foreign_key="user.id")
    course_id: UUID | None = Field(default=None, foreign_key="course.id")

    title: str | None = None
    agent: str | None = None

    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

    user: "User" = Relationship(back_populates="threads")
    course: "Course" = Relationship(back_populates="threads")
    messages: list["Message"] = Relationship(back_populates="thread")


class Message(SQLModel, table=True):
    id: UUID | None = Field(default_factory=uuid4, primary_key=True)

    thread_id: UUID = Field(foreign_key="thread.id")
    role: str
    content: str
    created_at: datetime = Field(default_factory=datetime.utcnow)

    thread: "Thread" = Relationship(back_populates="messages")

from datetime import datetime
from enum import StrEnum
from typing import TYPE_CHECKING
from uuid import UUID, uuid4

from sqlalchemy import Column, ForeignKey
from sqlalchemy import Enum as SAEnum
from sqlmodel import Field, Relationship, SQLModel


class ThreadTitleSource(StrEnum):
    DEFAULT = "default"
    GENERATED = "generated"
    MANUAL = "manual"


if TYPE_CHECKING:
    pass


class Thread(SQLModel, table=True):
    id: UUID | None = Field(default_factory=uuid4, primary_key=True)
    user_id: UUID = Field(
        sa_column=Column(ForeignKey("user.id", ondelete="CASCADE"), nullable=False)
    )
    title: str | None = None
    agent: str | None = None
    title_source: ThreadTitleSource | None = Field(
        default=ThreadTitleSource.DEFAULT,
        sa_column=Column(
            SAEnum(ThreadTitleSource, name="thread_title_source"),
            default=ThreadTitleSource.DEFAULT,
            nullable=True,
        ),
    )

    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

    messages: list["Message"] = Relationship(back_populates="thread")


class Message(SQLModel, table=True):
    id: UUID | None = Field(default_factory=uuid4, primary_key=True)
    thread_id: UUID = Field(foreign_key="thread.id")

    role: str
    content: str

    created_at: datetime = Field(default_factory=datetime.utcnow)

    thread: "Thread" = Relationship(back_populates="messages")

from datetime import UTC, datetime
from enum import StrEnum
from typing import TYPE_CHECKING
from uuid import UUID, uuid4

from pydantic import field_validator
from sqlalchemy import Column, ForeignKey, Text
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


def utc_now() -> datetime:
    return datetime.now(UTC)


class PromptBase(SQLModel):
    title: str = Field(
        min_length=1,
        max_length=150,
        description="Human-readable name of the prompt.",
    )
    description: str | None = Field(
        default=None,
        max_length=1000,
        description="Optional description of the prompt's purpose.",
    )

    content: str = Field(
        sa_column=Column(Text, nullable=False),
        description="The actual prompt text sent to the AI model.",
    )

    @field_validator("content")
    @classmethod
    def validate_content(cls, value: str) -> str:
        if not value.strip():
            raise ValueError("Prompt content cannot be empty.")

        if len(value) > 100_000:
            raise ValueError("Prompt exceeds maximum length.")

        return value


class Prompt(PromptBase, table=True):
    __tablename__ = "prompts"

    id: UUID = Field(
        default_factory=uuid4,
        primary_key=True,
    )

    user_id: UUID = Field(
        foreign_key="user.id",
        index=True,
        nullable=False,
    )

    created_at: datetime = Field(
        default_factory=utc_now,
    )

    updated_at: datetime = Field(
        default_factory=utc_now,
        sa_column_kwargs={"onupdate": utc_now},
    )


class PromptUpdate(PromptBase):
    title: str | None = Field(
        min_length=1,
        max_length=150,
        description="Human-readable name of the prompt.",
    )
    description: str | None = Field(
        default=None,
        max_length=1000,
        description="Optional description of the prompt's purpose.",
    )

    content: str | None = Field(
        default=None,
        sa_column=Column(Text, nullable=False),
        description="The actual prompt text sent to the AI model.",
    )

    @field_validator("content")
    @classmethod
    def validate_content(cls, value: str) -> str:
        if not value.strip():
            raise ValueError("Prompt content cannot be empty.")

        if len(value) > 100_000:
            raise ValueError("Prompt exceeds maximum length.")

        return value


class PromptSummary(SQLModel):
    id: UUID
    title: str
    description: str | None = None

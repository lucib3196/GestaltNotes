from datetime import datetime
from uuid import UUID, uuid4

from sqlalchemy import Column, DateTime
from sqlmodel import Field, SQLModel


class AnnouncementBase(SQLModel):
    title: str = Field(
        min_length=1,
        max_length=150,
        description="Short heading shown to recipients.",
    )
    message: str = Field(
        min_length=1,
        max_length=5000,
        description="Announcement content shown to recipients.",
    )
    version: str = Field(
        min_length=1,
        max_length=50,
        description="App version associated with this announcement, such as 1.2.0.",
    )
    audience_summary: str | None = Field(
        default=None,
        max_length=255,
        description="Human-readable summary of the intended audience, such as 'All students'.",
    )
    published: bool = Field(
        default=False,
        description="Whether this announcement is visible to recipients.",
    )


class AnnoucementUpdate(SQLModel):
    title: str | None = Field(
        default=None,
        min_length=1,
        max_length=150,
        description="Short heading shown to recipients.",
    )
    message: str | None = Field(
        default=None,
        min_length=1,
        max_length=5000,
        description="Announcement content shown to recipients.",
    )
    version: str | None = Field(
        default=None,
        min_length=1,
        max_length=50,
        description="App version associated with this announcement, such as 1.2.0.",
    )
    published: bool = Field(
        default=False,
        description="Whether this announcement is visible to recipients.",
    )


class Announcement(AnnouncementBase, table=True):
    __tablename__ = "announcements"  # type: ignore

    id: UUID = Field(default_factory=uuid4, primary_key=True)

    published_at: datetime | None = Field(
        default=None,
        sa_column=Column(DateTime(timezone=True), nullable=True),
        description="UTC time the announcement was published.",
    )


class AnnouncementRecipient(SQLModel, table=True):
    __tablename__ = "announcement_recipients"  # type: ignore

    announcement_id: UUID = Field(
        foreign_key="announcements.id",
        primary_key=True,
        ondelete="CASCADE",
    )
    user_id: UUID = Field(
        foreign_key="user.id",
        primary_key=True,
        ondelete="CASCADE",
    )
    read_at: datetime | None = Field(default=None)

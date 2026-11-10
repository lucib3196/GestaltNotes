from datetime import datetime
from uuid import UUID, uuid4
from pydantic import BaseModel
from sqlalchemy import Column, DateTime
from sqlmodel import Field, SQLModel
from datetime import UTC, datetime


def utc_now() -> datetime:
    return datetime.now(UTC)


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
    created_by_id: UUID | None = Field(
        default=None,
        foreign_key="user.id",
        nullable=True,
        ondelete="SET NULL",
        index=True,
    )
    created_at: datetime | None = Field(
        default=datetime.utcnow,
        sa_column=Column(DateTime(timezone=True), nullable=True),
    )
    created_at: datetime = Field(
        default_factory=utc_now,
        sa_column=Column(
            DateTime(timezone=True),
            nullable=False,
            default=utc_now,
        ),
    )

    updated_at: datetime = Field(
        default_factory=utc_now,
        sa_column=Column(
            DateTime(timezone=True),
            nullable=False,
            default=utc_now,
            onupdate=utc_now,
        ),
    )
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


class AnnouncementAudiencePreview(BaseModel):
    announcement_id: UUID
    published: bool
    total_users: int
    existing_recipients: int
    new_recipients: int
    read_recipients: int
    unread_recipients: int
    conflicting_recipients: int = 0


class AnnouncementHistoryItem(BaseModel):
    announcement: Announcement
    read_at: datetime | None


class AnnouncementHistoryPage(BaseModel):
    items: list[AnnouncementHistoryItem]
    total: int
    limit: int
    offset: int

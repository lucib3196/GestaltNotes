from enum import StrEnum
from uuid import UUID

from sqlalchemy import Column, ForeignKey
from sqlmodel import Field, SQLModel


class VectorStoreStatus(StrEnum):
    PENDING = "pending"
    READY = "ready"
    FAILED = "failed"
    ARCHIVED = "archieved"


class CourseVectorStore(SQLModel, table=True):
    __tablename__ = "course_vector_store"  # type: ignore

    course_id: UUID = Field(
        sa_column=Column(
            ForeignKey("course.id", ondelete="CASCADE"),
            nullable=False,
            primary_key=True,
        )
    )
    namespace_key: str = Field(unique=True, nullable=False)
    collection_name: str = Field(nullable=False)
    description: str | None = Field(default=None)
    embedding_model: str
    provider: str
    status: VectorStoreStatus

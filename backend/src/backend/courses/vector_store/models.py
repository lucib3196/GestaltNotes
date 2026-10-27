from enum import StrEnum
from typing import TYPE_CHECKING
from uuid import UUID

from sqlalchemy import Column, ForeignKey
from sqlalchemy import Enum as SAEnum
from sqlmodel import Field, Relationship, SQLModel

if TYPE_CHECKING:
    from backend.courses.models import Course


class VectorStoreStatus(StrEnum):
    PENDING = "pending"
    READY = "ready"
    FAILED = "failed"
    ARCHIVED = "archieved"


class VectorstoreProvider(StrEnum):
    ASTRA = "astra"
    POSTGRES = "postgres"


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
    provider: VectorstoreProvider = Field(
        sa_column=Column(
            SAEnum(VectorstoreProvider, name="vector_store_provider"),
            nullable=False,
        ),
    )
    status: VectorStoreStatus = Field(
        sa_column=Column(
            SAEnum(VectorStoreStatus, name="vector_store_status"),
            nullable=False,
        ),
    )

    # Attributes
    course: "Course" = Relationship(back_populates="vectorstore")

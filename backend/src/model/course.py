from sqlmodel import SQLModel, Field
from typing import Optional
from uuid import uuid4, UUID
from pydantic import BaseModel


class Course(SQLModel, table=True):
    id: Optional[UUID] = Field(default_factory=uuid4, primary_key=True)
    name: str
    discipline: str
    blob: str | None = Field(
        default=None, description="Location to store data for cloud storage"
    )
    description: str | None = Field(default=None)


class CourseData(BaseModel):
    name: str
    discipline: str
    blob: str | None
    description: str | None

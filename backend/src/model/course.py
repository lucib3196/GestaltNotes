from sqlmodel import SQLModel, Field
from typing import Optional
from uuid import uuid4, UUID


class Course(SQLModel, table=True):
    id: Optional[UUID] = Field(default_factory=uuid4, primary_key=True)
    name: str
    discipline: str
    description: str | None = Field(default=None)

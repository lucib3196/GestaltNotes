import datetime
from typing import TYPE_CHECKING
from uuid import UUID, uuid4

from pydantic import BaseModel
from sqlmodel import Field, Relationship, SQLModel

class CourseData(BaseModel):
    name: str
    discipline: str
    blob: str | None
    description: str | None
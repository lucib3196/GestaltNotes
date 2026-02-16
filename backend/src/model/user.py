from sqlmodel import SQLModel, Field
from typing import Optional
from uuid import uuid4, UUID
from pydantic import BaseModel


class UserCreate(BaseModel):
    first_name: str
    last_name: str
    password: str
    email: str


class UserLogin(BaseModel):
    email: str
    password: str


class UserRead(BaseModel):
    email: str


class User(SQLModel, table=True):
    id: Optional[UUID] = Field(default_factory=uuid4, primary_key=True)
    first_name: str
    last_name: str
    email: str

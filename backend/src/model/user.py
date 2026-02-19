
from sqlmodel import SQLModel, Field as SqlField, Relationship as SQLMODELRelationship
from typing import Optional, Literal
from uuid import uuid4, UUID
from pydantic import BaseModel
from datetime import datetime


VALID_ROLES = Literal["educator", "student", "admin"]


class UserRoleLink(SQLModel, table=True):
    user_id: UUID = SqlField(foreign_key="user.id", primary_key=True)
    role_id: UUID = SqlField(foreign_key="role.id", primary_key=True)


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
    id: Optional[UUID] = SqlField(default_factory=uuid4, primary_key=True)
    first_name: str
    last_name: str
    email: str
    roles: list["Role"] = SQLMODELRelationship(
        back_populates="users",
        link_model=UserRoleLink,
    )
    threads: list["Thread"] = SQLMODELRelationship(back_populates="user")


class Role(SQLModel, table=True):
    id: UUID = SqlField(default_factory=uuid4, primary_key=True)
    name: str = SqlField(index=True, unique=True)

    users: list[User] = SQLMODELRelationship(
        back_populates="roles",
        link_model=UserRoleLink,
    )

class Thread(SQLModel, table=True):
    id: Optional[UUID] = SqlField(default_factory=uuid4, primary_key=True)
    user_id: UUID = SqlField(foreign_key="user.id")
    title: Optional[str] = None
    created_at: datetime = SqlField(default_factory=datetime.utcnow)
    
    user: Optional[User] = SQLMODELRelationship(back_populates="threads")
    messages: list["Message"] = SQLMODELRelationship(back_populates="thread")

# might be doing 1 to 1 but need to do many to many because of forgein key
# 

class Message(SQLModel, table=True):
    id: Optional[UUID] = SqlField(default_factory=uuid4, primary_key=True)
    thread_id: UUID = SqlField(foreign_key="thread.id")
    role: str 
    content: str
    created_at: datetime = SqlField(default_factory=datetime.utcnow)
    
    thread: Optional[Thread] = SQLMODELRelationship(back_populates="messages")
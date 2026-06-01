from typing import TYPE_CHECKING, Literal
from uuid import UUID, uuid4

from pydantic import BaseModel, EmailStr
from sqlmodel import Field as SqlField
from sqlmodel import Relationship as SQLMODELRelationship
from sqlmodel import SQLModel

if TYPE_CHECKING:
    from .chat import Thread
    from .course import Course

VALID_ROLES = Literal["educator", "student", "admin"]


class UserRoleLink(SQLModel, table=True):
    user_id: UUID = SqlField(foreign_key="user.id", primary_key=True)
    role_id: UUID = SqlField(foreign_key="role.id", primary_key=True)


class UserCourseLink(SQLModel, table=True):
    user_id: UUID = SqlField(foreign_key="user.id", primary_key=True)
    course_id: UUID = SqlField(foreign_key="course.id", primary_key=True)


class UserLogin(BaseModel):
    email: EmailStr
    password: str


class UserBase(BaseModel):
    first_name: str | None = None
    last_name: str | None = None
    username: str | None = None


class UserCreate(UserBase):
    password: str
    email: EmailStr
    role: VALID_ROLES = "student"
    course_id: UUID | None = None


class UserRead(UserBase):
    email: str | None = None
    force_password_reset: bool = False
    roles: list[VALID_ROLES] = []


class UserUpdate(UserBase):
    email: str | None = None


class User(SQLModel, table=True):
    id: UUID | None = SqlField(default_factory=uuid4, primary_key=True)
    first_name: str | None = None
    last_name: str | None = None
    username: str | None = None
    email: EmailStr = SqlField(unique=True)
    roles: list["Role"] = SQLMODELRelationship(
        back_populates="users",
        link_model=UserRoleLink,
    )
    threads: list["Thread"] = SQLMODELRelationship(back_populates="user")
    courses: list["Course"] = SQLMODELRelationship(
        back_populates="educators",
        link_model=UserCourseLink,
    )


class Role(SQLModel, table=True):
    id: UUID = SqlField(default_factory=uuid4, primary_key=True)
    name: str = SqlField(index=True, unique=True)

    users: list[User] = SQLMODELRelationship(
        back_populates="roles",
        link_model=UserRoleLink,
    )


class StudentResponse(BaseModel):
    id: UUID
    first_name: str | None
    last_name: str | None
    email: str

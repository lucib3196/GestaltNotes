from enum import StrEnum
from uuid import UUID, uuid4

from pydantic import EmailStr
from sqlalchemy import Column, Enum
from sqlmodel import Field, Relationship, SQLModel


class UserRole(StrEnum):
    STUDENT = "student"
    EDUCATOR = "educator"
    ADMIN = "admin"


class UserRoleLink(SQLModel, table=True):
    __tablename__ = "user_role_link"  # type: ignore
    user_id: UUID = Field(foreign_key="user.id", primary_key=True)
    role_id: UUID = Field(foreign_key="role.id", primary_key=True)


class Role(SQLModel, table=True):
    id: UUID = Field(default_factory=uuid4, primary_key=True)
    name: UserRole = Field(
        sa_column=Column(
            Enum(UserRole, name="user_role"),
            nullable=False,
            unique=True,
            index=True,
        )
    )

    users: list[User] = Relationship(
        back_populates="roles",
        link_model=UserRoleLink,
    )


class User(SQLModel, table=True):
    id: UUID | None = Field(default_factory=uuid4, primary_key=True)
    first_name: str | None = None
    last_name: str | None = None
    username: str | None = None
    email: EmailStr = Field(unique=True)
    roles: list["Role"] = Relationship(
        back_populates="users",
        link_model=UserRoleLink,
    )

from uuid import UUID

from pydantic import BaseModel, EmailStr

from backend.accounts.models import UserRole

VALID_ROLES = UserRole


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
    role: UserRole = UserRole.STUDENT


class UserRead(UserBase):
    email: str | None = None
    force_password_reset: bool = False
    roles: list[UserRole] = []


class UserUpdate(UserBase):
    email: str | None = None


class StudentResponse(BaseModel):
    id: UUID
    first_name: str | None
    last_name: str | None
    email: str

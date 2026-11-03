from typing import Protocol
from uuid import uuid4

import pytest_asyncio
from pytest import fixture
from sqlmodel import Session, select

from backend.accounts import Role, User, UserCreate, UserRole
from backend.accounts.services import AccountService, RoleDB


class FakeAccountService:
    def __init__(self):
        return None

    async def create_account(self, data: UserCreate, role: UserRole) -> User:
        return User(
            email=data.email,
            first_name=data.first_name,
            last_name=data.last_name,
            roles=[self._resolve_role(role)],
        )

    def _resolve_role(self, role: UserRole) -> Role:
        return Role(name=role)

    async def delete_account(self, user_id: str):
        return None


@fixture
def fake_account_service():
    return FakeAccountService()


@fixture
def account_service(db_session, request, fake_account_service):
    service_kind = getattr(request, "param", "real")
    if service_kind == "real":
        request.getfixturevalue("firebase_app_for_tests")
        return AccountService(db_session)
    return fake_account_service


@pytest_asyncio.fixture(autouse=True)
async def seed_roles(_clean_db, db_session):
    return await RoleDB(db_session).seed_roles()


class MakeUserPayload(Protocol):
    def __call__(self, **overrides) -> UserCreate: ...


@fixture
def make_user_payload() -> MakeUserPayload:
    def make(**overrides) -> UserCreate:

        default_user = {
            "first_name": "luci",
            "last_name": "berm",
            "username": "luci123",
            "password": "string",
            "email": "lberm@email.com",
        }
        return UserCreate(**{**default_user, **overrides})

    return make


class MakeUser(Protocol):
    async def __call__(
        self,
        *,
        role: UserRole = UserRole.STUDENT,
        first_name: str = "Test",
        last_name: str = "User",
        username: str | None = None,
        email: str | None = None,
    ) -> User: ...


@fixture
def make_user(db_session: Session, seed_roles) -> MakeUser:
    """Persist a test user and role without registering with Firebase."""

    async def make(
        *,
        role: UserRole = UserRole.STUDENT,
        first_name: str = "Test",
        last_name: str = "User",
        username: str | None = None,
        email: str | None = None,
    ) -> User:
        suffix = uuid4().hex
        role_record = db_session.exec(select(Role).where(Role.name == role)).one()

        user = User(
            first_name=first_name,
            last_name=last_name,
            username=username if username is not None else f"user-{suffix}",
            email=email if email is not None else f"user-{suffix}@example.com",
            roles=[role_record],
        )
        db_session.add(user)
        db_session.commit()
        return user

    return make

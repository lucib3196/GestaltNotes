from backend.accounts.services import AccountService
import backend.core
from pytest import fixture
import pytest
import pytest_asyncio
from typing import Protocol
from backend.accounts import UserCreate, UserRole, User, Role
from backend.accounts.services import RoleDB
from uuid import uuid4


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
    roles = await RoleDB(db_session).seed_roles()
    return roles


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
        self, *, role: UserRole = UserRole.STUDENT, **overrides
    ) -> User: ...


@pytest_asyncio.fixture
async def make_user(account_service) -> MakeUser:
    created_users: list[User] = []

    async def make(*, role: UserRole = UserRole.STUDENT, **overrides):
        default_user = {
            "first_name": "luci",
            "last_name": "berm",
            "username": "luci123",
            "password": "string",
            "email": "lberm@email.com",
            "role": role,
        }
        user = await account_service.create_account(
            UserCreate(**{**default_user, **overrides}),
            role=role,
        )
        created_users.append(user)

        return user

    yield make
    for user in created_users:
        await account_service.delete_account(user.id)

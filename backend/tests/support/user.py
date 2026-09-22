from backend.accounts.services import AccountService
from pytest import fixture
from typing import Protocol
from backend.accounts import UserCreate


@fixture
def account_service(db_session):
    return AccountService(db_session)


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

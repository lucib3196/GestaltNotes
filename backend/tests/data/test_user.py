import pytest
from sqlmodel import Session

from src.service.user import UserDB


@pytest.fixture
def user_db(db_session: Session):
    return UserDB(db_session)


@pytest.mark.asyncio
async def test_user(user_db) -> None:
    print("Testing users")

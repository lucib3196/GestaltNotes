from src.data.user import UserDB
import pytest

@pytest.fixture
def user_db(db_session):
    return UserDB(db_session)

@pytest.mark.asyncio
async def test_user(user_db):
    print("Testing users")
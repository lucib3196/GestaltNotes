import pytest
import pytest_asyncio

from src.model.user import User, UserCreate, UserUpdate
from src.service.user import UserDB
from src.service.user.exceptions import UserCreationError, UserNotFoundError

from user_examples import USERS


@pytest.fixture
def user_create_examples() -> list[UserCreate]:
    return USERS


@pytest_asyncio.fixture
async def created_users(user_db: UserDB, user_create_examples: list[UserCreate]):
    return [await user_db.create_user(user) for user in user_create_examples]


@pytest.mark.asyncio
@pytest.mark.parametrize("u", USERS)
async def test_create_user_raise_error_on_duplicate_email(user_db: UserDB, u):
    # Create the user the first time
    await user_db.create_user(u)
    with pytest.raises(UserCreationError):
        await user_db.create_user(u)


@pytest.mark.asyncio
@pytest.mark.parametrize("u", USERS)
async def test_create_user_persists_user(user_db: UserDB, u: UserCreate) -> None:
    user = await user_db.create_user(u)

    assert user is not None
    assert user.id is not None
    assert user.first_name == u.first_name
    assert user.last_name == u.last_name
    assert user.email == u.email


@pytest.mark.asyncio
async def test_get_user_returns_user_by_id(
    user_db: UserDB, created_users: list[User]
) -> None:
    for _i, u in enumerate(created_users):
        assert u.id
        found_user = await user_db.get_user(u.id)

        assert found_user is not None
        assert found_user.id == u.id
        assert found_user.email == u.email


@pytest.mark.asyncio
async def test_get_user_by_email_strips_input(
    user_db: UserDB, created_users: list[User]
) -> None:

    for i, _u in enumerate(created_users):
        user = created_users[i]

        found_user = await user_db.get_user_by_email(f"  {user.email}  ")

        assert found_user is not None
        assert found_user.id == user.id
        assert found_user.email == user.email


@pytest.mark.asyncio
async def test_update_user_updates_only_provided_fields(
    user_db: UserDB, created_users
) -> None:
    user = created_users[2]
    update = UserUpdate(first_name="Kat", email="kat@example.com")

    updated_user = await user_db.update_user(user.id, update)

    assert updated_user.id == user.id
    assert updated_user.first_name == "Kat"
    assert updated_user.last_name == "Johnson"
    assert updated_user.email == "kat@example.com"


@pytest.mark.asyncio
async def test_delete_user_removes_user(
    user_db: UserDB, created_users: list[User]
) -> None:
    for i, _u in enumerate(created_users):
        user = created_users[i]
        assert user.id

        deleted = await user_db.delete_user(user.id)

        assert deleted is True
        assert await user_db.get_user(user.id) is None


@pytest.mark.asyncio
async def test_delete_user_raises_when_user_does_not_exist(
    user_db: UserDB, created_users
) -> None:
    missing_id = created_users[0].id
    await user_db.delete_user(missing_id)

    with pytest.raises(UserNotFoundError):
        await user_db.delete_user(missing_id)

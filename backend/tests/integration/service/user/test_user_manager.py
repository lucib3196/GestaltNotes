import pytest
import pytest_asyncio
from firebase_admin import auth
from firebase_admin.auth import UserRecord
from firebase_admin.auth import UserNotFoundError as FBUserNotFoundError
from sqlmodel import Session

from src.data.role import RoleDB
from src.model.user import User, UserCreate, UserUpdate
from src.service.user import UserManager
from src.service.user.exceptions import UserNotFoundError

from tests.integration.service.user.user_examples import USERS, ROLES


@pytest_asyncio.fixture
async def user_manager(db_session: Session, verify_firebase_emulator) -> UserManager:
    await RoleDB(db_session).seed_roles()
    return UserManager(db_session)


@pytest.fixture
def user_create_examples() -> list[UserCreate]:
    return USERS


@pytest_asyncio.fixture
async def created_users(
    user_manager: UserManager, user_create_examples: list[UserCreate]
):
    users: list[User] = []
    try:
        for user_create in user_create_examples:
            users.append(
                await user_manager.create_user(user_create, role=user_create.role)
            )
        yield users
    finally:
        for user in users:
            if user.id:
                await user_manager.rollback_user(user.id)


@pytest.mark.asyncio
@pytest.mark.parametrize("u", USERS)
async def test_create_user_persists_db_firebase_and_role(
    user_manager: UserManager, u: UserCreate
) -> None:
    user = await user_manager.create_user(u, role=u.role)

    try:
        assert user.id is not None
        assert user.first_name == u.first_name
        assert user.last_name == u.last_name
        assert user.email == u.email

        db_user = await user_manager._udb.get_user(user.id)
        assert db_user is not None
        assert db_user.id == user.id

        fb_user: UserRecord = auth.get_user(str(user.id))
        assert fb_user.uid == str(user.id)
        assert fb_user.email == u.email
        assert fb_user.custom_claims == {"force_password_reset": True}

        roles = await user_manager.get_user_roles(user.id)
        assert roles == [u.role]
    finally:
        if user.id:
            await user_manager.rollback_user(user.id)


@pytest.mark.asyncio
@pytest.mark.parametrize("u", USERS)
async def test_create_user_default_role_student(
    user_manager: UserManager, u: UserCreate
) -> None:
    user = await user_manager.create_user(u)

    try:
        assert user.id is not None
        roles = await user_manager.get_user_roles(user.id)
        assert roles
        assert "student" in roles
    finally:
        if user.id:
            await user_manager.rollback_user(user.id)


@pytest.mark.asyncio
@pytest.mark.parametrize("u", USERS)
@pytest.mark.parametrize("r", ROLES)
async def test_create_user_with_role(
    user_manager: UserManager, u: UserCreate, r
) -> None:
    user = await user_manager.create_user(u, role=r)

    try:
        assert user.id is not None
        roles = await user_manager.get_user_roles(user.id)
        assert roles
        assert r in roles
    finally:
        if user.id:
            await user_manager.rollback_user(user.id)


@pytest.mark.asyncio
async def test_get_user_returns_read_model_with_roles(
    user_manager: UserManager, created_users: list[User]
) -> None:
    user = created_users[0]
    assert user.id is not None

    found_user = await user_manager.get_user(user.id)

    assert found_user.first_name == user.first_name
    assert found_user.last_name == user.last_name
    assert found_user.email == user.email
    assert found_user.roles == ["student"]


@pytest.mark.asyncio
async def test_update_user_updates_and_returns_read_model(
    user_manager: UserManager, created_users: list[User]
) -> None:
    user = created_users[1]
    assert user.id is not None

    updated_user = await user_manager.update_user(
        user.id, UserUpdate(first_name="Amazing", email="amazing@example.com")
    )

    assert updated_user.first_name == "Amazing"
    assert updated_user.last_name == user.last_name
    assert updated_user.email == "amazing@example.com"


@pytest.mark.asyncio
async def test_delete_user_removes_database_user_only(
    user_manager: UserManager, created_users: list[User]
) -> None:
    user = created_users[2]
    assert user.id is not None

    await user_manager.delete_user(user.id)

    with pytest.raises(UserNotFoundError):
        await user_manager.get_user(user.id)

    fb_user = auth.get_user(str(user.id))
    assert fb_user.uid == str(user.id)

    await user_manager.rollback_fb(user.id)


@pytest.mark.asyncio
async def test_rollback_user_removes_db_and_firebase(
    user_manager: UserManager, user_create_examples: list[UserCreate]
) -> None:
    user = await user_manager.create_user(user_create_examples[0])

    assert user.id is not None

    await user_manager.rollback_user(user.id)
    await user_manager.ensure_user_rolled_back(user.id)

    assert await user_manager._udb.get_user(user.id) is None
    with pytest.raises(FBUserNotFoundError):
        auth.get_user(str(user.id))


@pytest.mark.asyncio
async def test_rollback_helpers_are_idempotent(user_manager: UserManager) -> None:
    missing_id = "00000000-0000-0000-0000-000000000000"

    assert await user_manager.rollback_db(missing_id) is True
    assert await user_manager.rollback_fb(missing_id) is True
    await user_manager.ensure_user_rolled_back(missing_id)

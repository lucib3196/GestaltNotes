import pytest
import pytest_asyncio
from firebase_admin import auth
from firebase_admin.auth import UserNotFoundError as FBUserNotFoundError
from firebase_admin.auth import UserRecord
from sqlmodel import Session

from backend.accounts.exceptions import UserNotFoundError
from backend.accounts.models import User, UserRole
from backend.accounts.schema import UserCreate, UserUpdate
from backend.accounts.services.role import RoleDB
from backend.accounts.services.user import AccountService

ROLES: list[UserRole] = [
    UserRole.ADMIN,
    UserRole.EDUCATOR,
    UserRole.STUDENT,
]

USERS: list[UserCreate] = [
    UserCreate(
        first_name="Ada",
        last_name="Lovelace",
        username="ada",
        email="ada@example.com",
        password="password-1",
    ),
    UserCreate(
        first_name="Grace",
        last_name="Hopper",
        username="grace",
        email="grace@example.com",
        password="password-2",
    ),
    UserCreate(
        first_name="Katherine",
        last_name="Johnson",
        username="katherine",
        email="katherine@example.com",
        password="password-3",
    ),
]


@pytest_asyncio.fixture
async def account_service(
    db_session: Session,
    firebase_app_for_tests,
) -> AccountService:
    await RoleDB(db_session).seed_roles()
    return AccountService(db_session)


@pytest.fixture
def user_create_examples() -> list[UserCreate]:
    return USERS


@pytest_asyncio.fixture
async def created_accounts(
    account_service: AccountService,
    user_create_examples: list[UserCreate],
):
    users: list[User] = []
    try:
        for user_create in user_create_examples:
            users.append(
                await account_service.create_account(user_create, role=user_create.role)
            )
        yield users
    finally:
        for user in users:
            if user.id:
                await account_service._rollback_account_creation(user.id)


@pytest.mark.asyncio
@pytest.mark.parametrize("user_create", USERS)
async def test_create_account_persists_db_firebase_and_role(
    account_service: AccountService,
    user_create: UserCreate,
) -> None:
    user = await account_service.create_account(user_create, role=user_create.role)

    try:
        assert user.id is not None
        assert user.first_name == user_create.first_name
        assert user.last_name == user_create.last_name
        assert user.email == user_create.email

        db_user = await account_service.get_account_orm(user.id)
        assert db_user.id == user.id

        fb_user: UserRecord = auth.get_user(str(user.id))
        assert fb_user.uid == str(user.id)
        assert fb_user.email == user_create.email
        assert fb_user.custom_claims == {"force_password_reset": True}

        roles = await account_service.list_roles(user.id)
        assert roles == [user_create.role]
    finally:
        if user.id:
            await account_service._rollback_account_creation(user.id)


@pytest.mark.asyncio
@pytest.mark.parametrize("user_create", USERS)
async def test_create_account_default_role_student(
    account_service: AccountService,
    user_create: UserCreate,
) -> None:
    user = await account_service.create_account(user_create)

    try:
        assert user.id is not None
        assert await account_service.list_roles(user.id) == [UserRole.STUDENT]
    finally:
        if user.id:
            await account_service._rollback_account_creation(user.id)


@pytest.mark.asyncio
@pytest.mark.parametrize("user_create", USERS)
@pytest.mark.parametrize("role", ROLES)
async def test_create_account_with_role(
    account_service: AccountService,
    user_create: UserCreate,
    role: UserRole,
) -> None:
    user = await account_service.create_account(user_create, role=role)

    try:
        assert user.id is not None
        assert await account_service.list_roles(user.id) == [role]
    finally:
        if user.id:
            await account_service._rollback_account_creation(user.id)


@pytest.mark.asyncio
async def test_get_account_returns_read_model_with_roles(
    account_service: AccountService,
    created_accounts: list[User],
) -> None:
    user = created_accounts[0]
    assert user.id is not None

    found_user = await account_service.get_account(user.id)

    assert found_user.first_name == user.first_name
    assert found_user.last_name == user.last_name
    assert found_user.email == user.email
    assert found_user.roles == [UserRole.STUDENT]


@pytest.mark.asyncio
async def test_get_account_by_email_strips_input(
    account_service: AccountService,
    created_accounts: list[User],
) -> None:
    user = created_accounts[0]

    found_user = await account_service.get_account_by_email(f"  {user.email}  ")

    assert found_user is not None
    assert found_user.id == user.id


@pytest.mark.asyncio
async def test_update_account_updates_and_returns_read_model(
    account_service: AccountService,
    created_accounts: list[User],
) -> None:
    user = created_accounts[1]
    assert user.id is not None

    updated_user = await account_service.update_account(
        user.id,
        UserUpdate(first_name="Amazing", email="amazing@example.com"),
    )

    assert updated_user.first_name == "Amazing"
    assert updated_user.last_name == user.last_name
    assert updated_user.email == "amazing@example.com"


@pytest.mark.asyncio
async def test_delete_account_removes_database_and_firebase_user(
    account_service: AccountService,
    created_accounts: list[User],
) -> None:
    user = created_accounts.pop()
    assert user.id is not None

    await account_service.delete_account(user.id)

    with pytest.raises(UserNotFoundError):
        await account_service.get_account_orm(user.id)

    with pytest.raises(FBUserNotFoundError):
        auth.get_user(str(user.id))


@pytest.mark.asyncio
async def test_rollback_account_creation_removes_db_and_firebase(
    account_service: AccountService,
    user_create_examples: list[UserCreate],
) -> None:
    user = await account_service.create_account(user_create_examples[0])
    assert user.id is not None

    await account_service._rollback_account_creation(user.id)

    with pytest.raises(UserNotFoundError):
        await account_service.get_account_orm(user.id)

    with pytest.raises(FBUserNotFoundError):
        auth.get_user(str(user.id))


@pytest.mark.asyncio
async def test_rollback_account_creation_is_idempotent(
    account_service: AccountService,
) -> None:
    missing_id = "00000000-0000-0000-0000-000000000000"

    await account_service._rollback_account_creation(missing_id)

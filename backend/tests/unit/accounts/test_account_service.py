from types import SimpleNamespace
from unittest.mock import patch

import pytest

from backend.accounts.models import UserRole
from backend.accounts.services.role import RoleDB
from backend.accounts.services.user import AccountService


@pytest.mark.asyncio
async def test_create_account_creates_db_user_assigns_role_and_calls_firebase(
    db_session,
    make_user_payload,
):
    await RoleDB(db_session).seed_roles()
    service = AccountService(db_session)
    payload = make_user_payload(role=UserRole.STUDENT)

    with patch(
        "backend.accounts.services.user.auth.create_user"
    ) as mock_create_user, patch(
        "backend.accounts.services.user.auth.set_custom_user_claims"
    ) as mock_claims:
        mock_create_user.side_effect = lambda **kwargs: SimpleNamespace(
            uid=kwargs["uid"]
        )

        user = await service.create_account(payload)

    assert user.id is not None
    assert user.first_name == payload.first_name
    assert user.last_name == payload.last_name
    assert user.username == payload.username
    assert user.email == payload.email

    saved_user = await service.get_account_orm(user.id)
    assert saved_user.id == user.id
    assert [role.name for role in saved_user.roles] == [UserRole.STUDENT]

    mock_create_user.assert_called_once_with(
        email=payload.email,
        display_name=payload.username,
        uid=str(user.id),
        password=payload.password,
    )
    mock_claims.assert_called_once_with(
        str(user.id),
        {"force_password_reset": True},
    )


@pytest.mark.asyncio
async def test_create_account_can_skip_force_password_reset_claim(
    db_session,
    make_user_payload,
):
    await RoleDB(db_session).seed_roles()
    service = AccountService(db_session)
    payload = make_user_payload(email="noreset@example.com")

    with patch(
        "backend.accounts.services.user.auth.create_user"
    ) as mock_create_user, patch(
        "backend.accounts.services.user.auth.set_custom_user_claims"
    ) as mock_claims:
        mock_create_user.side_effect = lambda **kwargs: SimpleNamespace(
            uid=kwargs["uid"]
        )

        user = await service.create_account(
            payload,
            role=UserRole.STUDENT,
            force_password_reset=False,
        )

    assert user.id is not None
    assert await service.get_account_orm(user.id)

    mock_create_user.assert_called_once()
    mock_claims.assert_not_called()

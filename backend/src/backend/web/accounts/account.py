from uuid import UUID

from fastapi.exceptions import HTTPException
from fastapi.responses import Response
from fastapi.routing import APIRouter
from firebase_admin import auth
from pydantic import BaseModel
from starlette import status

from backend.accounts.exceptions import UserNotFoundError, UserServiceException
from backend.accounts.models import User, UserRole
from backend.accounts.schema import (
    UserCreate,
    UserRead,
)
from backend.core import logger

from .dependencies import AccountServiceDependency, CurrentUser, FireBaseToken

ID = UUID | str

router = APIRouter(prefix="/users", tags=["users"])


class PasswordUpdate(BaseModel):
    new_password: str


class LoginRequest(BaseModel):
    id_token: str


@router.post("/")
async def create_user(
    account_service: AccountServiceDependency, data: UserCreate
) -> User:
    try:
        return await account_service.create_account(data, role=data.role)
    except HTTPException:
        raise
    except UserServiceException as e:
        raise HTTPException(status_code=400, detail=f"Failed to create user {e}") from e
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"User creation failed. {e}") from e


@router.post("/get_current_user")
async def get_current_user(
    current_user: CurrentUser,
    token: FireBaseToken,
    account_service: AccountServiceDependency,
) -> UserRead:
    try:
        user = await account_service.get_account(current_user)
        user.force_password_reset = token.get(
            "force_password_reset",
            False,
        )
        return user
    except UserNotFoundError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Failed to retrieve user {e}",
        ) from e
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to retrieve user information {e}",
        ) from None


@router.post("/login")
async def login(payload: LoginRequest) -> UserRead:
    decoded = auth.verify_id_token(payload.id_token)
    return UserRead(
        email=decoded.get("email", None),
        force_password_reset=decoded.get("force_password_reset", False),
    )


@router.post("/password_reset/temp")
async def password_reset(
    account_service: AccountServiceDependency,
    user_id: CurrentUser,
    update: PasswordUpdate,
) -> Response:
    try:
        account_service.reset_password(user_id, update.new_password)
        return Response(status_code=200, content="Updated password okay")
    except UserServiceException as e:
        raise HTTPException(status_code=500, detail=str(e)) from e


# ---------- ID-based user management
# These endpoints operate directly on internal user IDs and are intended for
# service/admin workflows rather than frontend token-based self-service paths.


@router.get("/{id}")
async def get_user_by_id(account_service: AccountServiceDependency, id: ID) -> UserRead:
    """
    Retrieve a user by internal ID.

    This endpoint is intended for backend/admin flows where user IDs are
    already known.
    """
    try:
        return await account_service.get_account(id)

    except UserServiceException as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Failed to retrieve user {e}",
        ) from e
    except Exception as e:
        logger.exception("Failed to retrieve user by id='%s'", id)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to retrieve user '{id}': {e}",
        ) from e


@router.delete("/{id}")
async def delete_user_by_id(
    account_service: AccountServiceDependency, id: ID
) -> dict[str, str]:
    """
    Delete a user by internal ID.

    This endpoint is intended for backend/admin flows.
    """
    try:
        await account_service.delete_account(id)
        return {"detail": "user deleted"}
    except UserServiceException as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Failed to delete user {e}",
        ) from e
    except Exception as e:
        logger.exception("Failed to delete user id='%s'", id)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to delete user '{id}': {e}",
        ) from e


@router.post("/{id}/roles")
async def set_user_role(
    account_service: AccountServiceDependency, id: ID, role: UserRole
) -> User:
    try:
        return await account_service.assign_role(id, role)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to add role {e}",
        ) from e

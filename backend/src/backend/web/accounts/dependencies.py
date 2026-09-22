from typing import Annotated, Any

from fastapi import Depends, HTTPException
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from firebase_admin.auth import (
    ExpiredIdTokenError,
    InvalidIdTokenError,
    verify_id_token,
)
from starlette import status

from backend.accounts.exceptions import UserNotFoundError
from backend.accounts.models import User, UserRole
from backend.accounts.services.user import AccountService
from backend.core.logger import logger
from backend.database import SessionDep

bearer_scheme = HTTPBearer(auto_error=False)


def get_firebase_user_from_token(
    token: Annotated[HTTPAuthorizationCredentials | None, Depends(bearer_scheme)],
) -> dict[str, Any]:
    """Validate bearer token and return decoded Firebase claims."""
    if not token or not token.credentials:
        logger.info("Authentication failed: missing bearer token")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Missing authentication token",
            headers={"WWW-Authenticate": "Bearer"},
        )

    try:
        return verify_id_token(token.credentials)
    except (InvalidIdTokenError, ExpiredIdTokenError) as e:
        logger.info("Authentication failed: invalid/expired Firebase token (%s)", e)
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired authentication token",
            headers={"WWW-Authenticate": "Bearer"},
        ) from e
    except Exception as e:
        logger.exception("Authentication failed: token verification error")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Authentication failed",
            headers={"WWW-Authenticate": "Bearer"},
        ) from e


FireBaseToken = Annotated[dict[str, Any], Depends(get_firebase_user_from_token)]


def get_current_user_id(
    token: FireBaseToken,
) -> str:
    """Extract authenticated user id from decoded Firebase claims."""
    user_id = token.get("user_id")
    if not user_id:
        logger.warning("Token is valid but missing 'user_id' claim")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Authenticated token is missing required user identifier",
        )
    return user_id


CurrentUser = Annotated[str, Depends(get_current_user_id)]


def get_account_service(session: SessionDep) -> AccountService:
    """Create an AccountService scoped to the current request session."""
    try:
        return AccountService(session)
    except Exception as e:
        logger.exception("Failed to initialize AccountService")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to initialize account service",
        ) from e


AccountServiceDependency = Annotated[AccountService, Depends(get_account_service)]


async def get_current_user(
    user_id: CurrentUser,
    account_service: AccountServiceDependency,
) -> User:
    """Load current user record from the database."""
    try:
        return await account_service.get_account_orm(user_id)
    except UserNotFoundError as e:
        logger.info("Authenticated user not found in database: user_id=%s", user_id)
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User not found"
        ) from e
    except Exception as e:
        logger.exception(
            "Failed to load current user from database: user_id=%s", user_id
        )
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to load current user",
        ) from e


CurrentUserDep = Annotated[User, Depends(get_current_user)]


def require_student(user: CurrentUserDep) -> User:
    """Ensure current user has student role."""
    if not any(r.name == UserRole.STUDENT for r in user.roles):
        logger.info(
            "Authorization denied: student role required for user_id=%s", user.id
        )
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="Student access required"
        )
    return user


def require_educator(user: CurrentUserDep) -> User:
    """Ensure current user has educator role."""
    if not any(r.name == UserRole.EDUCATOR for r in user.roles):
        logger.info(
            "Authorization denied: educator role required for user_id=%s", user.id
        )
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="Educator access required"
        )
    return user


StudentDep = Annotated[User, Depends(require_student)]
EducatorDep = Annotated[User, Depends(require_educator)]

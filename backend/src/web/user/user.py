from uuid import UUID

from fastapi.exceptions import HTTPException
from fastapi.responses import Response
from fastapi.routing import APIRouter
from firebase_admin import auth
from pydantic import BaseModel
from sqlmodel import select
from starlette import status

from src.core import logger
from src.core.database_config import SessionDep
from src.model.course import Course
from src.model.user import (
    VALID_ROLES,
    Role,
    StudentResponse,
    User,
    UserCreate,
    UserRead,
    UserRoleLink,
)
from src.service.user.exceptions import UserNotFoundError, UserServiceException

from .dependencies import (
    CurrentUser,
    UserManagerDependency,
)

ID = UUID | str

router = APIRouter(prefix="/users", tags=["users"])


class PasswordUpdate(BaseModel):
    new_password: str


class LoginRequest(BaseModel):
    id_token: str


@router.post("/")
async def create_user(
    user_manager: UserManagerDependency, data: UserCreate, session: SessionDep
) -> User:
    try:
        user = await user_manager.create_user(data, role=data.role)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Unexpected Error User is None",
            )
        # TODO eventually move this logic somewhere else
        if data.course_id and data.role == "educator":
            course = session.get(Course, data.course_id)
            if not course:
                raise HTTPException(status_code=404, detail="Course not found")
            course.educators.append(user)
            session.commit()
        return user
    except HTTPException:
        raise
    except UserServiceException as e:
        raise HTTPException(status_code=400, detail=f"Failed to create user {e}") from e
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"User creation failed. {e}")


@router.post("/get_current_user")
async def get_current_user(
    current_user: CurrentUser,
    user_manager: UserManagerDependency,
) -> UserRead:
    try:
        return await user_manager.get_user(current_user)
    except UserNotFoundError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Failed to retrieve user {e}",
        ) from e
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to retrieve user information",
        ) from None


@router.post("/login")
async def login(payload: LoginRequest):
    decoded = auth.verify_id_token(payload.id_token)
    return UserRead(
        email=decoded.get("email", None),
        force_password_reset=decoded.get("force_password_reset", False),
    )


@router.post("/password_reset/temp")
async def password_reset(user_id: CurrentUser, update: PasswordUpdate) -> Response:
    try:
        auth.update_user(uid=user_id, password=update.new_password)
        auth.set_custom_user_claims(str(user_id), {"force_password_reset": False})
        return Response(status_code=200, content="Updated password okay")
    except Exception:
        raise HTTPException(status_code=500, detail="Failed to update password")


# ---------- ID-based user management
# These endpoints operate directly on internal user IDs and are intended for
# service/admin workflows rather than frontend token-based self-service paths.


@router.get("/{id}")
async def get_user_by_id(
    user_manager: UserManagerDependency, id: ID
) -> UserRead | None:
    """
    Retrieve a user by internal ID.

    This endpoint is intended for backend/admin flows where user IDs are
    already known.
    """
    try:
        return await user_manager.get_user(id)

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
async def delete_user_by_id(user_manager: UserManagerDependency, id: ID):
    """
    Delete a user by internal ID.

    This endpoint is intended for backend/admin flows.
    """
    try:
        user = await user_manager.get_user(id)
        assert user
        await user_manager.delete_user(id)
        return {"detail": "user deleted"}
    except UserServiceException as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Failed to retrieve user {e}",
        ) from e
    except Exception as e:
        logger.exception("Failed to delete user id='%s'", id)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to delete user '{id}': {e}",
        ) from e


@router.post("/{id}/roles")
async def set_user_role(
    user_manager: UserManagerDependency, id: ID, role: VALID_ROLES
) -> User:
    try:
        user = await user_manager.set_user_roles(id, role)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Failed to add role, user is not defined",
            )
        return user
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to add role {e}",
        )


# -----------------Other
# These endpoints not sure if they are active or not
#


@router.get("/students", response_model=list[StudentResponse])
def get_students(session: SessionDep):
    return session.exec(
        select(User)
        .join(UserRoleLink, UserRoleLink.user_id == User.id)
        .join(Role, Role.id == UserRoleLink.role_id)
        .where(Role.name == "student")
    ).all()

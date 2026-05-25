import requests
from fastapi.exceptions import HTTPException
from fastapi.responses import Response
from fastapi.routing import APIRouter
from firebase_admin import auth
from pydantic import BaseModel
from sqlmodel import select
from starlette import status

from src.core.database_config import SessionDep
from src.model.chat import Thread, ThreadCreate
from src.model.course import Course
from src.model.user import (
    Role,
    StudentResponse,
    User,
    UserCreate,
    UserRead,
    UserRoleLink,
)
from src.web.dependencies import (
    CurrentUser,
    CurrentUserDep,
    FireBaseToken,
    StudentDep,
    ThreadDBDependency,
)

from .dependencies import UserManagerDependency


class PasswordUpdate(BaseModel):
    new_password: str


router = APIRouter(prefix="/users", tags=["users"])


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
        if data.course_id and data.role == "educator":
            course = session.get(Course, data.course_id)
            if not course:
                raise HTTPException(status_code=404, detail="Course not found")
            course.educators.append(user)
            session.commit()

        return user
    except Exception as e:
        if "EMAIL_EXISTS" in str(e):
            raise HTTPException(
                status_code=400, detail="User with this email already exists."
            )
        raise HTTPException(status_code=400, detail=f"User creation failed. {e}")


@router.post("/login")
async def login(payload: LoginRequest):
    decoded = auth.verify_id_token(payload.id_token)
    return UserRead(
        email=decoded.get("email", None),
        force_password_reset=decoded.get("force_password_reset", False),
    )


@router.post("/get_current_user")
def get_current_user(
    token: FireBaseToken,
) -> UserRead:
    decoded = token
    return UserRead(email=decoded.get("email", None))


@router.post("/password_reset/temp")
async def password_reset(user_id: CurrentUser, update: PasswordUpdate) -> Response:
    try:
        auth.update_user(uid=user_id, password=update.new_password)
        auth.set_custom_user_claims(str(user_id), {"force_password_reset": False})
        return Response(status_code=200, content="Updated password okay")
    except Exception:
        raise HTTPException(status_code=500, detail="Failed to update password")


@router.get("/thread")
async def get_user_threads(
    token: FireBaseToken, thread_db: ThreadDBDependency
) -> list[Thread]:
    try:
        user_id = token.get("user_id", None)
        if user_id is None:
            raise HTTPException(
                detail="Failed to retrieve signed in user",
                status_code=status.HTTP_400_BAD_REQUEST,
            )
        return await thread_db.list_threads_for_user(user_id, None)
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to create user {e}")


@router.post("/thread")
async def create_user_thread(
    token: FireBaseToken,
    thread_db: ThreadDBDependency,
    user: StudentDep,
    data: ThreadCreate | None = None,
) -> Thread:
    try:
        user_id = token.get("user_id", None)
        if user_id is None:
            raise HTTPException(
                detail="Failed to retrieve signed in user",
                status_code=status.HTTP_400_BAD_REQUEST,
            )
        if data:
            thread = await thread_db.create_thread(
                thread_id=data.thread_id,
                course_id=data.course_id,
                title=data.title,
                agent=data.agent,
                user_id=user_id,
            )
        else:
            thread = await thread_db.create_thread(user_id=user_id)
        return thread
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to create thread {e}")


# @router.post()
@router.post("/login_test")
def emulator_login(email: str, password: str):
    """Testing endpoint for login using password and email

    Args:
        email (str):
        password (str):

    Returns:
        _type_: _description_
    """
    url = "http://127.0.0.1:9099/identitytoolkit.googleapis.com/v1/accounts:signInWithPassword?key=fake-key"

    payload = {"email": email, "password": password, "returnSecureToken": True}

    response = requests.post(url, json=payload)
    return response.json()


@router.get("/me")
async def get_me(user: CurrentUserDep):
    return {
        "id": user.id,
        "first_name": user.first_name,
        "last_name": user.last_name,
        "email": user.email,
        "roles": [r.name for r in user.roles],
    }


@router.get("/students", response_model=list[StudentResponse])
def get_students(session: SessionDep):
    return session.exec(
        select(User)
        .join(UserRoleLink, UserRoleLink.user_id == User.id)
        .join(Role, Role.id == UserRoleLink.role_id)
        .where(Role.name == "student")
    ).all()

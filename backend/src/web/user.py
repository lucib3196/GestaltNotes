from .dependencies import UserManagerDependency
from src.model.user import UserLogin, UserCreate, UserRead, User
from fastapi.routing import APIRouter
from fastapi.exceptions import HTTPException
from starlette import status
from firebase_admin import auth
import requests

router = APIRouter(prefix="/users", tags=["users"])


@router.post("/")
async def create_user(user_manager: UserManagerDependency, data: UserCreate) -> User:
    try:
        user = await user_manager.create_user(data)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Unexpected Error User is None",
            )
        return user
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail={str(e)})


@router.post("/login")
async def login(id_token: str):
    decoded = auth.verify_id_token(id_token)
    user_read = UserRead(email=decoded.get("email", None))
    return user_read


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

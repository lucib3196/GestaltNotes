from functools import lru_cache
from typing import Annotated, Dict, Any

from fastapi import Depends, HTTPException
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from firebase_admin.auth import verify_id_token
from starlette import status

from src.core.database_config import SessionDep
from src.core.logger import logger
from src.core.settings import get_settings
from src.data.course import CourseDB
from src.data.message import MessageDB
from src.data.thread import ThreadDB
from src.service import FirebaseStorage
from src.service.user.user_manager import UserManager
from src.model.user import User


bearer_scheme = HTTPBearer(auto_error=False)


def get_firebase_user_from_token(
    token: Annotated[HTTPAuthorizationCredentials | None, Depends(bearer_scheme)],
) -> Dict[str, str] | None:
    try:
        if not token:
            raise ValueError("No Token")
        return verify_id_token(token.credentials)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=f"Not logged in or Invalid credentials {str(e)}",
            headers={"WWW-Authenticate": "Bearer"},
        )


FireBaseToken = Annotated[Dict[str, str], Depends(get_firebase_user_from_token)]


def get_current_user_id(
    token: FireBaseToken,
) -> str:
    try:
        user_id = token.get("user_id", None)
        if user_id is None:
            raise HTTPException(
                detail="Failed to retrieve signed in user",
                status_code=status.HTTP_400_BAD_REQUEST,
            )
        return user_id
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            detail=f"Failed to retrieve signed in user {e}",
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )


CurrentUser = Annotated[str, Depends(get_current_user_id)]


@lru_cache
def get_firebase_storage() -> FirebaseStorage:
    settings = get_settings()
    if not (settings.FIREBASE_CRED and settings.STORAGE_BUCKET):
        raise ValueError("Settings for Cloud Storage not Set")
    storage_service = FirebaseStorage(
        bucket=settings.STORAGE_BUCKET,
    )

    logger.debug(f"Question manager set to {settings.STORAGE_SERVICE}")
    logger.debug("Initialized Question Manager Success")

    return storage_service


FbStorageDependency = Annotated[FirebaseStorage, Depends(get_firebase_storage)]


@lru_cache
def get_user_manager(session: SessionDep) -> UserManager:
    try:
        logger.debug("Initializing UserDB")

        return UserManager(session)
    except Exception as e:
        raise ValueError("Failed to initialize userdb")


UserManagerDependency = Annotated[UserManager, Depends(get_user_manager)]


@lru_cache
def get_course_db(session: SessionDep) -> CourseDB:
    try:
        logger.debug("Initialized Course DB")
        return CourseDB(session)
    except Exception as e:
        raise ValueError("Failed to initialize Course DB")


CourseDBDependency = Annotated[CourseDB, Depends(get_course_db)]


@lru_cache
def get_thread_db(session: SessionDep) -> ThreadDB:
    try:
        logger.debug("Initialized Thread DB")
        return ThreadDB(session)
    except Exception as e:
        raise ValueError("Failed to initialize Thread DB")


ThreadDBDependency = Annotated[ThreadDB, Depends(get_thread_db)]


@lru_cache
def get_message_db(session: SessionDep) -> MessageDB:
    try:
        logger.debug("Initialized Message DB")
        return MessageDB(session)
    except Exception as e:
        raise ValueError("Failed to initialize Message DB")


MessageDBDependency = Annotated[MessageDB, Depends(get_message_db)]

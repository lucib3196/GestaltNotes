from src.service import FirebaseStorage
from functools import lru_cache
from typing import Annotated
from src.core.database_config import SessionDep
from src.core.settings import get_settings
from fastapi import Depends
from src.core.logger import logger
from src.service.user.user_manager import UserManager
from src.data.course import CourseDB


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

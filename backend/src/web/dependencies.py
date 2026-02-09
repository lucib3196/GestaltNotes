from src.service import FirebaseStorage
from functools import lru_cache
from typing import Annotated
from src.core import get_settings
from fastapi import Depends, HTTPException
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from starlette import status
from src.core import logger

from firebase_admin.auth import verify_id_token


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


FirebaseDependency = Annotated[FirebaseStorage, Depends(get_firebase_storage)]

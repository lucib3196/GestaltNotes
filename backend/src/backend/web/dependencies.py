from functools import lru_cache
from typing import Annotated

from fastapi import Depends

from backend.core.logger import logger
from backend.core.settings import get_settings
from backend.data.message import MessageDB
from backend.database import SessionDep
from backend.service import FirebaseStorage


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
def get_message_db(session: SessionDep) -> MessageDB:
    try:
        logger.debug("Initialized Message DB")
        return MessageDB(session)
    except Exception:
        raise ValueError("Failed to initialize Message DB")


MessageDBDependency = Annotated[MessageDB, Depends(get_message_db)]

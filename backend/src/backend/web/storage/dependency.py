from backend.storage import (
    FileService,
    FileRepository,
    FirebaseBlobStorage,
    BlobStorage,
)
from backend.core import get_settings
from backend.web.dependencies import SessionDep
from typing import Annotated

from fastapi import Depends, HTTPException

settings = get_settings()


def get_storage() -> BlobStorage:
    assert settings.STORAGE_BUCKET
    return FirebaseBlobStorage(settings.STORAGE_BUCKET)


def get_file_service(session: SessionDep, storage: "StorageDep") -> FileService:
    return FileService(session=session, storage=storage)


StorageDep = Annotated[BlobStorage, Depends(get_storage)]

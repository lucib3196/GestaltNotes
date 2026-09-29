from typing import Annotated

from fastapi import Depends

from backend.core import get_settings
from backend.storage import (
    BlobStorage,
    FileService,
    FirebaseBlobStorage,
)
from backend.web.dependencies import SessionDep

settings = get_settings()


def get_storage() -> BlobStorage:
    assert settings.STORAGE_BUCKET
    return FirebaseBlobStorage(settings.STORAGE_BUCKET)


def get_file_service(session: SessionDep, storage: "StorageDep") -> FileService:
    return FileService(session=session, storage=storage)


StorageDep = Annotated[BlobStorage, Depends(get_storage)]
FileServiceDep = Annotated[FileService, Depends(get_file_service)]

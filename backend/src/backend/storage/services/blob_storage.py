from typing import BinaryIO, Protocol

from backend.storage.models import BlobMetadata

BlobUploadData = BinaryIO | bytes | str


class BlobStorage(Protocol):
    async def upload(
        self,
        key: str,
        data: BlobUploadData,
        content_type: str | None = None,
    ) -> None: ...

    async def download(
        self,
        key: str,
    ) -> bytes: ...

    async def delete(
        self,
        key: str,
    ) -> None: ...

    async def exists(
        self,
        key: str,
    ) -> bool: ...

    async def directory_exists(
        self,
        key: str,
    ) -> bool: ...

    async def create_directory(
        self,
        key: str,
    ) -> None: ...

    async def list_directory(
        self,
        key: str,
        recursive: bool = False,
    ) -> list["BlobMetadata"]: ...

    async def delete_directory(
        self,
        key: str,
    ) -> None: ...

    async def get_metadata(
        self,
        key: str,
    ) -> "BlobMetadata": ...

    async def get_download_url(
        self,
        key: str,
    ) -> str: ...

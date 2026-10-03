from typing import BinaryIO, Protocol

from backend.storage.blob.schema import BlobMetadata

BlobUploadData = BinaryIO | bytes | str


class BlobStorage(Protocol):
    """Storage interface for raw blob/object operations."""

    async def upload(
        self,
        key: str,
        data: BlobUploadData,
        content_type: str | None = None,
    ) -> None:
        """Upload data to an exact blob key."""
        ...

    async def download(
        self,
        key: str,
    ) -> bytes:
        """Download an exact blob as bytes."""
        ...

    async def delete(
        self,
        key: str,
    ) -> None:
        """Delete an exact blob if supported by the backend."""
        ...

    async def exists(
        self,
        key: str,
    ) -> bool:
        """Return whether an exact blob exists."""
        ...

    async def directory_exists(
        self,
        key: str,
    ) -> bool:
        """Return whether a directory-like prefix contains blobs."""
        ...

    async def create_directory(
        self,
        key: str,
    ) -> None:
        """Create a directory-like placeholder blob."""
        ...

    async def list_directory(
        self,
        key: str,
        recursive: bool = False,
    ) -> list["BlobMetadata"]:
        """List blobs under a directory-like prefix."""
        ...

    async def delete_directory(
        self,
        key: str,
    ) -> None:
        """Delete all blobs under a directory-like prefix."""
        ...

    async def get_metadata(
        self,
        key: str,
    ) -> "BlobMetadata":
        """Return metadata for an exact blob."""
        ...

    async def get_download_url(
        self,
        key: str,
    ) -> str:
        """Return a downloadable URL for an exact blob."""
        ...

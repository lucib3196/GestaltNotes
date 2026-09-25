from backend.storage.exceptions import (
    BlobDirectoryNotFoundError,
    BlobNotFoundError,
    BlobStorageDeleteError,
    BlobStorageDirectoryError,
    BlobStorageMetadataError,
    BlobStorageReadError,
    BlobStorageUploadError,
    InvalidBlobKeyError,
)
from backend.storage.models import BlobMetadata
from firebase_admin import storage
from google.cloud.storage.blob import Blob

from .blob_storage import BlobStorage, BlobUploadData


class FirebaseBlobStorage(BlobStorage):
    def __init__(self, bucket: str):
        self._bucket = storage.bucket(bucket)

    async def exists(self, key: str) -> bool:
        return bool(self._bucket.get_blob(self._to_blob_key(key)))

    async def upload(
        self, key: str, data: BlobUploadData, content_type: str | None = None
    ) -> None:
        blob_key = self._to_blob_key(key)
        try:
            blob: Blob = self._bucket.blob(blob_key)
            blob.upload_from_string(
                self._read_upload_data(data),
                content_type=content_type or "application/octet-stream",
            )
        except Exception as e:
            raise BlobStorageUploadError(f"Failed to upload blob '{blob_key}'") from e

    async def read(self, key: str) -> bytes:
        blob_key = self._to_blob_key(key)
        try:
            blob = self._bucket.get_blob(blob_key)
            if blob is None:
                raise BlobNotFoundError(blob_key)
            return blob.download_as_bytes()
        except BlobNotFoundError:
            raise
        except Exception as e:
            raise BlobStorageReadError(f"Failed to read blob '{blob_key}'") from e

    async def download(self, key: str) -> bytes:
        return await self.read(key)

    async def delete(self, key: str) -> None:
        blob_key = self._to_blob_key(key)
        try:
            blob = self._bucket.blob(blob_key)
            if blob.exists():
                blob.delete()
        except Exception as e:
            raise BlobStorageDeleteError(f"Failed to delete blob '{blob_key}'") from e

    async def directory_exists(self, key: str) -> bool:
        directory_key = self._to_directory_key(key)
        try:
            blobs = self._bucket.list_blobs(prefix=directory_key, max_results=1)
            return next(blobs, None) is not None
        except Exception as e:
            raise BlobStorageDirectoryError(
                f"Failed to check blob directory '{directory_key}'"
            ) from e

    async def create_directory(self, key: str) -> None:
        directory_key = self._to_directory_key(key)
        try:
            blob = self._bucket.blob(directory_key)
            blob.upload_from_string(b"", content_type="application/x-directory")
        except Exception as e:
            raise BlobStorageDirectoryError(
                f"Failed to create blob directory '{directory_key}'"
            ) from e

    async def list_directory(
        self,
        key: str,
        recursive: bool = False,
    ) -> list[BlobMetadata]:
        directory_key = self._to_directory_key(key)
        try:
            blobs = self._bucket.list_blobs(
                prefix=directory_key,
                delimiter=None if recursive else "/",
            )
            return [
                self._to_metadata(blob)
                for blob in blobs
                if blob.name != directory_key
            ]
        except Exception as e:
            raise BlobStorageDirectoryError(
                f"Failed to list blob directory '{directory_key}'"
            ) from e

    async def delete_directory(self, key: str) -> None:
        directory_key = self._to_directory_key(key)
        try:
            if not await self.directory_exists(directory_key):
                raise BlobDirectoryNotFoundError(directory_key)

            blobs = self._bucket.list_blobs(prefix=directory_key)
            for blob in blobs:
                blob.delete()
        except BlobDirectoryNotFoundError:
            raise
        except Exception as e:
            raise BlobStorageDirectoryError(
                f"Failed to delete blob directory '{directory_key}'"
            ) from e

    async def get_metadata(self, key: str) -> BlobMetadata:
        blob_key = self._to_blob_key(key)
        try:
            blob = self._bucket.get_blob(blob_key)
            if blob is None:
                raise BlobNotFoundError(blob_key)
            return self._to_metadata(blob)
        except BlobNotFoundError:
            raise
        except Exception as e:
            raise BlobStorageMetadataError(
                f"Failed to get metadata for blob '{blob_key}'"
            ) from e

    async def get_download_url(self, key: str) -> str:
        blob_key = self._to_blob_key(key)
        try:
            blob = self._bucket.get_blob(blob_key)
            if blob is None:
                raise BlobNotFoundError(blob_key)
            return blob.public_url
        except BlobNotFoundError:
            raise
        except Exception as e:
            raise BlobStorageReadError(
                f"Failed to get download URL for blob '{blob_key}'"
            ) from e

    def _to_metadata(self, blob: Blob) -> BlobMetadata:
        assert blob.name
        return BlobMetadata(
            key=blob.name,
            size=blob.size,
            content_type=blob.content_type,
            created_at=blob.time_created,
            updated_at=blob.updated,
        )

    def _to_blob_key(self, key: str | Blob) -> str:
        if isinstance(key, Blob):
            name = key.name
            if not name:
                raise InvalidBlobKeyError("Failed to convert blob to key: missing name")
        else:
            name = str(key)
        return name.replace("\\", "/").lstrip("/")

    def _to_directory_key(self, key: str | Blob) -> str:
        name = self._to_blob_key(key)
        if not name.endswith("/"):
            name = f"{name}/"
        return name

    def _read_upload_data(self, data: BlobUploadData) -> bytes | str:
        if isinstance(data, bytes | str):
            return data
        return data.read()

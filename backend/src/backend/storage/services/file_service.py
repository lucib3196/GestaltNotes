import contextlib
from pathlib import Path
from uuid import UUID

from backend.accounts.models import User
from backend.storage.blob.base import BlobStorage, BlobUploadData
from backend.storage.blob.exceptions import BlobStorageDeleteError
from backend.storage.blob.schema import BlobMetadata
from backend.storage.exceptions import (
    FileNotFoundError,
    FileRetrievalError,
    FileServiceCreateError,
    FileServiceDeletionError,
    FileServiceRetrievalError,
    FileServiceUpdateError,
)
from backend.storage.repo.file_repository import FileRepository
from backend.storage.repo.schema import File, FileUpdate


class FileService:
    def __init__(self, storage: BlobStorage, repo: FileRepository) -> None:
        self._storage = storage
        self._repo = repo

    async def create_file(
        self,
        owner: User | UUID,
        filename: str,
        data: BlobUploadData,
        content_type: str | None = None,
    ) -> File:
        """Upload blob data and persist the matching file metadata."""
        file_id = None
        try:
            await self._storage.upload(filename, data, content_type)
            metadata = await self._storage.get_metadata(filename)
            file_record = File(
                owner_id=self._resolve_user_id(owner),
                original_name=self._resolve_filename(filename),
                storage_key=filename,
                content_type=metadata.content_type or content_type,
                size_bytes=metadata.size,
            )
            file_id = file_record.id
            return await self._repo.create(file_record)
        except Exception as e:
            await self._rollback(filename, file_id)
            raise FileServiceCreateError(f"Failed to create file '{filename}'") from e

    async def get_file(
        self,
        file_id: UUID,
    ) -> File:
        """Return file metadata by id."""
        try:
            file = await self._repo.get(file_id)
            if file is None:
                raise FileNotFoundError(str(file_id))
            return file
        except FileNotFoundError:
            raise
        except Exception as e:
            raise FileServiceRetrievalError(f"Failed to get file '{file_id}'") from e

    async def get_file_metadata(
        self,
        file_id: UUID,
    ) -> BlobMetadata:
        """Return blob metadata for a persisted file."""
        try:
            file = await self.get_file(file_id)
            return await self._storage.get_metadata(file.storage_key)
        except FileNotFoundError:
            raise
        except Exception as e:
            raise FileServiceRetrievalError(
                f"Failed to get metadata for file '{file_id}'"
            ) from e

    async def get_download_url(
        self,
        file_id: UUID,
    ) -> str:
        """Return a downloadable URL for a persisted file."""
        try:
            file = await self.get_file(file_id)
            return await self._storage.get_download_url(file.storage_key)
        except FileNotFoundError:
            raise
        except Exception as e:
            raise FileServiceRetrievalError(
                f"Failed to get download URL for file '{file_id}'"
            ) from e

    async def replace_file(
        self,
        file_id: UUID,
        data: BlobUploadData,
        content_type: str | None = None,
    ) -> File:
        """Replace blob contents and refresh file metadata."""
        try:
            file = await self.get_file(file_id)
            await self._storage.upload(file.storage_key, data, content_type)
            metadata = await self._storage.get_metadata(file.storage_key)
            return await self._repo.update_by_id(
                file_id,
                FileUpdate(
                    content_type=metadata.content_type or content_type,
                    size_bytes=metadata.size,
                ),
            )
        except FileNotFoundError:
            raise
        except Exception as e:
            raise FileServiceUpdateError(f"Failed to replace file '{file_id}'") from e

    async def rename_file(
        self,
        file_id: UUID,
        name: str,
    ) -> File:
        """Move a blob to a new name and update file metadata."""
        try:
            file = await self.get_file(file_id)
            new_key = self._rename_storage_key(file.storage_key, name)

            data = await self._storage.download(file.storage_key)
            await self._storage.upload(new_key, data, file.content_type)
            await self._storage.delete(file.storage_key)

            file.storage_key = new_key
            file.original_name = self._resolve_filename(name)

            return await self._repo.update(file, FileUpdate())
        except FileNotFoundError:
            raise
        except Exception as e:
            raise FileServiceUpdateError(f"Failed to rename file '{file_id}'") from e

    async def delete_file(
        self,
        file_id: UUID,
    ) -> None:
        """Delete both blob data and file metadata."""
        try:
            file = await self.get_file(file_id)
            await self._storage.delete(file.storage_key)
            await self._repo.delete(file_id)
        except FileNotFoundError:
            raise
        except Exception as e:
            raise FileServiceDeletionError(f"Failed to delete file '{file_id}'") from e

    async def _rollback(self, filename: str, file_id: UUID | None) -> None:
        with contextlib.suppress(BlobStorageDeleteError):
            await self._storage.delete(filename)
        try:
            if not file_id:
                return
            await self._repo.delete(record_id=file_id)
        except FileRetrievalError:
            pass

    def _resolve_user_id(self, user: User | UUID) -> UUID:
        if isinstance(user, User):
            if not (user.id):
                raise ValueError("Failed to resolve user, missing id")
            return user.id
        return user

    def _resolve_filename(self, filename: str) -> str:
        return Path(filename).name

    def _rename_storage_key(self, storage_key: str, name: str) -> str:
        path = Path(storage_key)
        parent = path.parent.as_posix()
        filename = self._resolve_filename(name)
        if parent == ".":
            return filename
        return f"{parent}/{filename}"

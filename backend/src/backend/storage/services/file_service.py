from pathlib import Path
from uuid import UUID

from backend.accounts.models import User
from backend.storage.exceptions import (
    BlobStorageDeleteError,
    FileNotFoundError,
    FileRetrievalError,
    FileServiceCreateError,
    FileServiceDeletionError,
    FileServiceRetrievalError,
    FileServiceUpdateError,
)
from backend.storage.models import BlobMetadata, File, FileUpdate

from .blob_storage import BlobStorage, BlobUploadData
from .file_repository import FileRepository


class FileService:
    def __init__(self, storage: BlobStorage, repo: FileRepository):
        self._storage = storage
        self._repo = repo

    async def create_file(
        self,
        owner: User | UUID,
        filename: str,
        data: BlobUploadData,
        content_type: str | None = None,
    ) -> File:
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
        try:
            file = await self.get_file(file_id)
            await self._storage.delete(file.storage_key)
            await self._repo.delete(file_id)
        except FileNotFoundError:
            raise
        except Exception as e:
            raise FileServiceDeletionError(f"Failed to delete file '{file_id}'") from e

    async def _rollback(self, filename: str, file_id: UUID | None) -> None:
        try:
            await self._storage.delete(filename)
        except BlobStorageDeleteError:
            pass
        try:
            if not file_id:
                return
            await self._repo.delete(file_id=file_id)
        except FileRetrievalError:
            pass

    def _resolve_user_id(self, user: User | UUID) -> UUID:
        if isinstance(user, User):
            if not (user.id):
                raise ValueError("Failed to resolve user, missing id")
            return user.id
        else:
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

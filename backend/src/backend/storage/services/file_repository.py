from datetime import datetime
from uuid import UUID

from sqlalchemy.exc import SQLAlchemyError
from sqlmodel import Session, col, select

from backend.accounts.models import User
from backend.core import logger
from backend.storage.exceptions import (
    FileCreationError,
    FileDeletionError,
    FileNotFoundError,
    FileRetrievalError,
    FileUpdateError,
)
from backend.storage.models import File, FileUpdate

from .blob_storage import BlobStorage


class FileRepository:
    def __init__(self, session: Session, storage: BlobStorage):
        self._session = session
        self._storage = storage

    async def create(self, file: File) -> File:
        try:
            self._session.add(file)
            self._session.commit()
            self._session.refresh(file)
            return file
        except SQLAlchemyError as e:
            self._session.rollback()
            message = f"[FileRepository] failed to create file {e}"
            logger.error(message)
            raise FileCreationError(message) from e

    async def get(self, file_id: UUID) -> File | None:
        try:
            return self._session.exec(select(File).where(File.id == file_id)).first()
        except SQLAlchemyError as e:
            self._session.rollback()
            message = f"[FileRepository] failed to get file {e}"
            logger.error(message)
            raise FileRetrievalError(message) from e

    async def update(self, file: File, update: FileUpdate) -> File:
        try:
            for key, value in update.model_dump(exclude_unset=True).items():
                setattr(file, key, value)

            file.updated_at = datetime.utcnow()

            self._session.add(file)
            self._session.commit()
            self._session.refresh(file)
            return file
        except SQLAlchemyError as e:
            self._session.rollback()
            message = f"[FileRepository] failed to update file {e}"
            logger.error(message)
            raise FileUpdateError(message) from e

    async def update_by_id(self, file_id: UUID, update: FileUpdate) -> File:
        file = await self.get(file_id)

        if file is None:
            raise FileNotFoundError(str(file_id))

        return await self.update(file, update)

    async def delete(self, file_id: UUID) -> None:
        try:
            file = await self.get(file_id)

            if file is None:
                return

            self._session.delete(file)
            self._session.commit()
        except FileRetrievalError:
            raise
        except SQLAlchemyError as e:
            self._session.rollback()
            message = f"[FileRepository] failed to delete file {e}"
            logger.error(message)
            raise FileDeletionError(message) from e

    async def list_by_owner(self, owner: User) -> list[File]:
        try:
            statement = (
                select(File)
                .where(File.owner_id == owner.id)
                .order_by(col(File.created_at).desc())
            )
            return list(self._session.exec(statement).all())
        except SQLAlchemyError as e:
            self._session.rollback()
            message = f"[FileRepository] failed to list files by owner {e}"
            logger.error(message)
            raise FileRetrievalError(message) from e

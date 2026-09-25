from datetime import datetime
from uuid import UUID

from sqlalchemy.exc import SQLAlchemyError
from sqlmodel import Session, col, select

from backend.accounts.models import User
from backend.core import logger
from backend.storage.blob.base import BlobStorage
from backend.storage.repo.base import Repository
from backend.storage.repo.exceptions import (
    FileCreationError,
    FileDeletionError,
    FileNotFoundError,
    FileRetrievalError,
    FileUpdateError,
)
from backend.storage.repo.schema import File, FileUpdate


class FileRepository(Repository[File, FileUpdate, User]):
    def __init__(self, session: Session, storage: BlobStorage) -> None:
        self._session = session
        self._storage = storage

    async def create(self, record: File) -> File:
        """Persist a file metadata record."""
        try:
            self._session.add(record)
            self._session.commit()
            self._session.refresh(record)
            return record
        except SQLAlchemyError as e:
            self._session.rollback()
            message = f"[FileRepository] failed to create file {e}"
            logger.error(message)
            raise FileCreationError(message) from e

    async def get(self, record_id: UUID) -> File | None:
        """Fetch a file metadata record by id."""
        try:
            return self._session.exec(select(File).where(File.id == record_id)).first()
        except SQLAlchemyError as e:
            self._session.rollback()
            message = f"[FileRepository] failed to get file {e}"
            logger.error(message)
            raise FileRetrievalError(message) from e

    async def update(self, record: File, update: FileUpdate) -> File:
        """Apply allowed metadata updates and bump updated_at."""
        try:
            for key, value in update.model_dump(exclude_unset=True).items():
                setattr(record, key, value)

            record.updated_at = datetime.utcnow()

            self._session.add(record)
            self._session.commit()
            self._session.refresh(record)
            return record
        except SQLAlchemyError as e:
            self._session.rollback()
            message = f"[FileRepository] failed to update file {e}"
            logger.error(message)
            raise FileUpdateError(message) from e

    async def update_by_id(self, record_id: UUID, update: FileUpdate) -> File:
        """Fetch a file metadata record by id and update it."""
        file = await self.get(record_id)

        if file is None:
            raise FileNotFoundError(str(record_id))

        return await self.update(file, update)

    async def delete(self, record_id: UUID) -> None:
        """Delete a file metadata record by id."""
        try:
            file = await self.get(record_id)

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
        """List file metadata records for an owner, newest first."""
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

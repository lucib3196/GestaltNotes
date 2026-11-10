from typing import Generic, TypeVar
from uuid import UUID

from pydantic import BaseModel
from sqlmodel import Session, SQLModel

RecordT = TypeVar("RecordT", bound=SQLModel)
UpdateT = TypeVar("UpdateT", bound=BaseModel)


class Repository(Generic[RecordT, UpdateT]):  # noqa: UP046 -- Support Python 3.11.
    """Shared CRUD operations within a caller-owned transaction."""

    def __init__(self, session: Session, model: type[RecordT]) -> None:
        self._session = session
        self._model = model

    async def create(self, record: RecordT) -> RecordT:
        """Stage a new record without committing."""
        self._session.add(record)
        self._session.flush()
        self._session.refresh(record)
        return record

    async def get(self, record_id: UUID) -> RecordT | None:
        """Fetch a record by id."""
        return self._session.get(self._model, record_id)

    async def update(self, record: RecordT, update: UpdateT) -> RecordT:
        """Apply an update to an existing record."""
        values = update.model_dump(exclude_unset=True)
        record.sqlmodel_update(values)
        self._session.add(record)
        self._session.flush()
        self._session.refresh(record)
        return record

    async def update_by_id(self, record_id: UUID, update: UpdateT) -> RecordT:
        """Fetch a record by id and apply an update."""
        record = await self.get(record_id)
        if record is None:
            raise LookupError(f"{self._model.__name__} {record_id} not found")
        return await self.update(record, update)

    async def delete(self, record_id: UUID) -> None:
        """Stage deletion of a record without committing."""
        record = await self.get(record_id)
        if record is None:
            return
        self._session.delete(record)
        self._session.flush()

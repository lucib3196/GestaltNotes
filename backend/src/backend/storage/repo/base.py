from typing import Protocol, TypeVar
from uuid import UUID

RecordT = TypeVar("RecordT")
UpdateT = TypeVar("UpdateT",contravariant=True)
OwnerT = TypeVar("OwnerT",contravariant=True)


class Repository(Protocol[RecordT, UpdateT, OwnerT]):
    """Generic persistence interface for storage records."""

    async def create(self, record: RecordT) -> RecordT:
        """Persist a new record."""
        ...

    async def get(self, record_id: UUID) -> RecordT | None:
        """Fetch a record by id."""
        ...

    async def update(self, record: RecordT, update: UpdateT) -> RecordT:
        """Apply an update to an existing record."""
        ...

    async def update_by_id(self, record_id: UUID, update: UpdateT) -> RecordT:
        """Fetch a record by id and apply an update."""
        ...

    async def delete(self, record_id: UUID) -> None:
        """Delete a record by id."""
        ...

    async def list_by_owner(self, owner: OwnerT) -> list[RecordT]:
        """List records belonging to an owner."""
        ...

from collections.abc import Sequence
from typing import Protocol, TypeVar
from uuid import UUID

RecordT = TypeVar("RecordT")
UpdateT = TypeVar("UpdateT", contravariant=True)


class Repository(Protocol[RecordT, UpdateT]):
    """Generic persistence interface for repositories"""

    async def create(self, record: RecordT) -> RecordT:
        """Persist a new record."""
        raise NotImplementedError(
            f"{type(self).__name__}.create() must be implemented by the repository."
        )

    async def get(self, record_id: UUID) -> RecordT | None:
        """Fetch a record by id."""
        raise NotImplementedError(
            f"{type(self).__name__}.get() must be implemented by the repository."
        )

    async def update(self, record: RecordT, update: UpdateT) -> RecordT:
        """Apply an update to an existing record."""
        raise NotImplementedError(
            f"{type(self).__name__}.update() must be implemented by the repository."
        )

    async def update_by_id(self, record_id: UUID, update: UpdateT) -> RecordT:
        """Fetch a record by id and apply an update."""
        raise NotImplementedError(
            f"{type(self).__name__}.update_by_id() must be implemented by the repository."
        )

    async def delete(self, record_id: UUID) -> None:
        """Delete a record by id."""
        raise NotImplementedError(
            f"{type(self).__name__}.delete() must be implemented by the repository."
        )

    async def list(self) -> Sequence[RecordT]:
        "List all records"
        raise NotImplementedError(
            f"{type(self).__name__}.list() must be implemented by the repository."
        )

from uuid import UUID

from backend.adapters import Repository


class FakeRepo[RecordT, UpdateT](Repository[RecordT, UpdateT]):
    def __init__(self, records: dict[UUID, RecordT] | None = None):
        self.records = dict(records) if records is not None else {}

    async def get(self, record_id: UUID) -> RecordT | None:
        return self.records.get(record_id)

    async def create(self, record: RecordT) -> RecordT:
        raise NotImplementedError("create is not supported by this fake")

    async def update(self, record: RecordT, update: UpdateT) -> RecordT:
        raise NotImplementedError("update is not supported by this fake")

    async def update_by_id(self, record_id: UUID, update: UpdateT) -> RecordT:
        raise NotImplementedError("update_by_id is not supported by this fake")

    async def delete(self, record_id: UUID) -> None:
        raise NotImplementedError("delete is not supported by this fake")

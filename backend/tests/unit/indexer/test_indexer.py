from unittest.mock import AsyncMock, Mock, call
from uuid import UUID, uuid4

import pytest
from langchain_core.documents import Document
from langchain_core.vectorstores import VectorStore
from pydantic import BaseModel, Field

from backend.indexer.indexer import DocumentBuilder, IndexingService
from tests.support.repository import FakeRepo


class FakeModel(BaseModel):
    id: UUID = Field(default_factory=uuid4)
    title: str
    content: str


class FakeDocumentBuilder(DocumentBuilder[FakeModel]):
    async def to_document(self, data: FakeModel) -> Document:
        return Document(
            id=str(data.id),
            page_content=data.content,
            metadata={"title": data.title},
        )


@pytest.fixture
def vector_store():
    store = Mock(spec=VectorStore)
    store.aget_by_ids = AsyncMock(return_value=[])
    store.aadd_documents = AsyncMock(return_value=[])
    store.adelete = AsyncMock(return_value=True)
    return store


@pytest.fixture
def fake_builder():
    return FakeDocumentBuilder()


@pytest.fixture
def fake_repo():
    data = [
        FakeModel(title="Lecture1", content="Some Content"),
        FakeModel(title="Lecture2", content="Some Content for Lecture 2"),
    ]
    return FakeRepo[FakeModel, FakeModel]({record.id: record for record in data})


@pytest.fixture
def fake_indexer(fake_builder, fake_repo, vector_store):
    return IndexingService(
        repo=fake_repo,
        builder=fake_builder,
        vector_store=vector_store,
    )


@pytest.mark.asyncio
async def test_builder_to_document(fake_builder):
    record = FakeModel(title="Lecture 1", content="Some notes")
    document = await fake_builder.to_document(record)
    assert document.page_content == "Some notes"
    assert document.metadata.get("title") == "Lecture 1"


@pytest.mark.asyncio
async def test_builder_build(fake_builder):
    data = [
        FakeModel(title="Lecture1", content="Some Content"),
        FakeModel(title="Lecture2", content="Some Content"),
    ]
    documents = await fake_builder.build(data)
    assert len(data) == len(documents)
    for record, document in zip(data, documents, strict=True):
        assert document.page_content == record.content
        assert document.metadata.get("title") == record.title


@pytest.mark.asyncio
async def test_index_writes_document(fake_indexer, fake_repo, vector_store):
    record_id, record = next(iter(fake_repo.records.items()))

    await fake_indexer.index(record_id)

    expected = Document(
        id=str(record_id),
        page_content=record.content,
        metadata={"title": record.title},
    )
    vector_store.aget_by_ids.assert_awaited_once_with([str(record_id)])
    vector_store.aadd_documents.assert_awaited_once_with(
        [expected],
        ids=[str(record_id)],
    )


@pytest.mark.asyncio
async def test_index_skips_unchanged_document(fake_indexer, fake_repo, vector_store):
    record_id, record = next(iter(fake_repo.records.items()))
    existing = Document(
        id=str(record_id),
        page_content=record.content,
        metadata={"title": record.title},
    )
    vector_store.aget_by_ids.return_value = [existing]
    await fake_indexer.index(record_id)
    vector_store.aget_by_ids.assert_awaited_once_with([str(record_id)])
    vector_store.aadd_documents.assert_not_awaited()


@pytest.mark.asyncio
async def test_index_updates_changed_content(fake_indexer, fake_repo, vector_store):
    record_id, record = next(iter(fake_repo.records.items()))
    old = Document(
        id=str(record_id),
        page_content="Old content",
        metadata={"title": record.title},
    )
    vector_store.aget_by_ids.return_value = [old]
    await fake_indexer.index(record_id)

    expected = Document(
        id=str(record_id),
        page_content=record.content,
        metadata={"title": record.title},
    )
    vector_store.aadd_documents.assert_awaited_once_with(
        [expected],
        ids=[str(record_id)],
    )


@pytest.mark.asyncio
async def test_index_updates_changed_metadata(fake_indexer, fake_repo, vector_store):
    record_id, record = next(iter(fake_repo.records.items()))
    old = Document(
        id=str(record_id),
        page_content=record.content,
        metadata={"title": "Old title"},
    )
    vector_store.aget_by_ids.return_value = [old]
    await fake_indexer.index(record_id)

    expected = Document(
        id=str(record_id),
        page_content=record.content,
        metadata={"title": record.title},
    )
    vector_store.aadd_documents.assert_awaited_once_with(
        [expected],
        ids=[str(record_id)],
    )


@pytest.mark.asyncio
async def test_index_force_recreates_unchanged_document(
    fake_indexer, fake_repo, vector_store
):
    record_id, record = next(iter(fake_repo.records.items()))
    expected = Document(
        id=str(record_id),
        page_content=record.content,
        metadata={"title": record.title},
    )
    vector_store.aget_by_ids.return_value = [expected]
    await fake_indexer.index(record_id, force_recreate=True)
    vector_store.aadd_documents.assert_awaited_once_with(
        [expected],
        ids=[str(record_id)],
    )


@pytest.mark.asyncio
async def test_delete_document(fake_indexer, fake_repo, vector_store):
    record_id = next(iter(fake_repo.records))
    assert await fake_indexer.delete([record_id]) is None
    vector_store.adelete.assert_awaited_once_with(
        ids=[str(record_id)],
    )


@pytest.mark.asyncio
async def test_delete_raises_when_vector_store_reports_failure(
    fake_indexer, fake_repo, vector_store
):
    record_id = next(iter(fake_repo.records))
    vector_store.adelete.return_value = False

    with pytest.raises(RuntimeError, match="Could not delete indexed resource"):
        await fake_indexer.delete([record_id])

    vector_store.adelete.assert_awaited_once_with(ids=[str(record_id)])


@pytest.mark.asyncio
@pytest.mark.parametrize("force_recreate", [False, True])
async def test_index_many_writes_unique_documents(
    fake_indexer, fake_repo, vector_store, force_recreate
):
    records = list(fake_repo.records.values())
    record_ids = [record.id for record in records]

    # Return the IDs supplied to each vector write.
    async def add_documents(documents, *, ids):
        return ids

    vector_store.aadd_documents.side_effect = add_documents

    # Existing identical documents should only be rewritten when forced.
    if force_recreate:
        existing = {
            str(record.id): Document(
                id=str(record.id),
                page_content=record.content,
                metadata={"title": record.title},
            )
            for record in records
        }

        async def get_documents(ids):
            return [existing[document_id] for document_id in ids]

        vector_store.aget_by_ids.side_effect = get_documents

    result = await fake_indexer.index_many(
        [*record_ids, record_ids[0]],
        force_recreate=force_recreate,
    )

    assert result == [str(record_id) for record_id in record_ids]
    assert vector_store.aget_by_ids.await_count == len(records)
    assert vector_store.aadd_documents.await_count == len(records)
    vector_store.aadd_documents.assert_has_awaits(
        [
            call(
                [
                    Document(
                        id=str(record.id),
                        page_content=record.content,
                        metadata={"title": record.title},
                    )
                ],
                ids=[str(record.id)],
            )
            for record in records
        ],
        any_order=True,
    )

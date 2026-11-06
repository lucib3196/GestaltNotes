from unittest.mock import Mock
from uuid import uuid4

import pytest
from pytest_mock import MockerFixture
from sqlmodel import Session

from backend.courses.models import NoteBlock, NoteBlockUpdate
from backend.courses.repo.note_blocks_repo import NoteBlockRepo
from backend.courses.service.note_block_service import NoteBlockService
from backend.indexer.indexer import IndexingService

pytestmark = pytest.mark.asyncio


@pytest.fixture
def indexer(mocker: MockerFixture):
    indexer = mocker.Mock(spec=IndexingService)
    indexer.index = mocker.AsyncMock(return_value=[])
    indexer.index_many = mocker.AsyncMock(return_value=[])
    indexer.delete = mocker.AsyncMock()
    return indexer


@pytest.fixture
def session():
    return Mock(spec=Session)


@pytest.fixture
def blocks():
    return Mock(spec=NoteBlockRepo)


@pytest.fixture
def service(session, blocks, indexer):
    return NoteBlockService(
        session=session,
        blocks=blocks,
        indexer=indexer,
    )


@pytest.fixture
def block():
    return NoteBlock(
        course_note_id=uuid4(),
        title="Newton's laws",
        kind="lecture_summary",
        position=0,
        content={
            "title": "Newton's laws",
            "summary": "Force changes momentum.",
            "topics": ["Force", "Momentum"],
            "objectives": ["Explain Newton's laws"],
            "prerequisites": [],
            "kind": "conceptual",
        },
    )


async def test_create_saves_and_indexes(service, blocks, indexer, session, block):
    # Return the validated record supplied by the service.
    blocks.create.side_effect = lambda record: record

    saved = await service.create(block)

    assert saved.id == block.id
    assert saved.content == block.content
    blocks.create.assert_awaited_once()
    session.commit.assert_called_once_with()
    indexer.index_many.assert_awaited_once_with([block.id])


async def test_create_many_empty_does_nothing(service, blocks, indexer, session):
    assert await service.create_many([]) == []

    blocks.create.assert_not_awaited()
    session.commit.assert_not_called()
    indexer.index_many.assert_not_awaited()


async def test_get_returns_block(service, blocks, block):
    blocks.get.return_value = block

    assert await service.get(block.id) is block

    blocks.get.assert_awaited_once_with(block.id)


async def test_update_saves_revision_and_reindexes(
    service, blocks, indexer, session, block
):
    blocks.get.return_value = block
    original_revision = block.revision

    async def apply_update(record, update):
        for field, value in update.model_dump(exclude_unset=True).items():
            setattr(record, field, value)
        return record

    blocks.update.side_effect = apply_update
    update = NoteBlockUpdate(title="Updated title")

    saved = await service.update(block.id, update)

    assert saved.title == "Updated title"
    assert saved.revision == original_revision + 1
    blocks.update.assert_awaited_once_with(block, update)
    session.commit.assert_called_once_with()
    indexer.index.assert_awaited_once_with(block.id)


async def test_delete_removes_vector_before_database_row(
    service, blocks, indexer, session, block
):
    blocks.get.return_value = block
    operations = Mock()
    operations.attach_mock(indexer.delete, "delete_vectors")
    operations.attach_mock(blocks.delete, "delete_row")
    operations.attach_mock(session.commit, "commit")

    await service.delete(block.id)

    from unittest.mock import call

    assert operations.mock_calls == [
        call.delete_vectors([block.id]),
        call.delete_row(block.id),
        call.commit(),
    ]


async def test_delete_vector_failure_preserves_database_row(
    service, blocks, indexer, session, block
):
    blocks.get.return_value = block
    indexer.delete.side_effect = RuntimeError("Vector store unavailable")

    with pytest.raises(RuntimeError, match="Vector store unavailable"):
        await service.delete(block.id)

    blocks.delete.assert_not_awaited()
    session.commit.assert_not_called()
    session.rollback.assert_called_once_with()


@pytest.mark.parametrize("force_recreate", [False, True])
async def test_reindex_delegates_without_saving(
    service, blocks, indexer, session, block, force_recreate
):
    blocks.get.return_value = block

    await service.reindex(block.id, force_recreate=force_recreate)

    indexer.index.assert_awaited_once_with(
        block.id,
        force_recreate=force_recreate,
    )
    blocks.update.assert_not_awaited()
    session.commit.assert_not_called()

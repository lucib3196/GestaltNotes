from types import SimpleNamespace
from unittest.mock import AsyncMock, Mock
from uuid import uuid4

import pytest

from backend.courses.service.course_note_service import CourseNoteService
from backend.courses.service.note_block_service import NoteBlockService


@pytest.mark.asyncio
@pytest.mark.parametrize("cleanup_fails", [False, True])
async def test_note_deletion_cleans_blocks_before_source_records(cleanup_fails):
    note_id, file_id, course_id = uuid4(), uuid4(), uuid4()
    events = []
    session = Mock()
    session.commit.side_effect = lambda: events.append("commit")

    async def delete_blocks(note_id, *, commit):
        assert commit is False
        events.append("blocks")
        if cleanup_fails:
            raise RuntimeError("Vector cleanup failed")

    async def delete_note(note_id):
        events.append("note")

    async def delete_file(file_id):
        events.append("file")
        return SimpleNamespace(storage_key="notes/source.pdf")

    async def delete_blob(storage_key):
        events.append("blob")

    notes = SimpleNamespace(
        get_required=AsyncMock(
            return_value=SimpleNamespace(file_id=file_id, course_id=course_id)
        ),
        delete=AsyncMock(side_effect=delete_note),
    )
    files = SimpleNamespace(
        stage_delete_file=AsyncMock(side_effect=delete_file),
        delete_blob=AsyncMock(side_effect=delete_blob),
    )
    service = CourseNoteService(
        session=session,
        notes=notes,
        blocks=SimpleNamespace(delete_by_note_id=AsyncMock(side_effect=delete_blocks)),
        files=files,
        access=SimpleNamespace(require_owner=AsyncMock()),
    )

    if cleanup_fails:
        with pytest.raises(RuntimeError, match="Vector cleanup failed"):
            await service.delete(note_id, user=Mock())
        assert events == ["blocks"]
        session.rollback.assert_called_once_with()
        session.commit.assert_not_called()
    else:
        await service.delete(note_id, user=Mock())
        assert events == ["blocks", "note", "file", "commit", "blob"]
        session.rollback.assert_not_called()


@pytest.mark.asyncio
@pytest.mark.parametrize("cleanup_fails", [False, True])
async def test_block_cleanup_leaves_transaction_to_caller(cleanup_fails):
    note_id = uuid4()
    block_ids = [uuid4(), uuid4()]
    session = Mock()
    blocks = SimpleNamespace(
        list_by_note=AsyncMock(
            return_value=[SimpleNamespace(id=block_id) for block_id in block_ids]
        ),
        delete=AsyncMock(),
    )
    indexer = SimpleNamespace(delete=AsyncMock())
    if cleanup_fails:
        indexer.delete.side_effect = RuntimeError("Vector cleanup failed")
    service = NoteBlockService(session=session, blocks=blocks, indexer=indexer)

    if cleanup_fails:
        with pytest.raises(RuntimeError, match="Vector cleanup failed"):
            await service.delete_by_note_id(note_id, commit=False)
        blocks.delete.assert_not_awaited()
    else:
        await service.delete_by_note_id(note_id, commit=False)
        assert [call.args[0] for call in blocks.delete.await_args_list] == block_ids

    indexer.delete.assert_awaited_once_with(block_ids)
    session.commit.assert_not_called()
    session.rollback.assert_not_called()

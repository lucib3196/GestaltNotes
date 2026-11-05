from unittest.mock import AsyncMock, Mock
from uuid import uuid4

import pytest
from sqlmodel import select

from backend.accounts.models import Role, User, UserRole
from backend.courses.exceptions import (
    CourseNoteDeletionConflictError,
    CourseNoteDeletionError,
    CourseOwnershipError,
)
from backend.courses.models import Course, CourseContentType, CourseNote, NoteBlock
from backend.courses.service import course_note_service as module
from backend.courses.service.course_note_service import CourseNoteService
from backend.processing.models import (
    LectureProcessingRun,
    ProcessingRun,
    ProcessingStage,
    ProcessingStatus,
)
from backend.storage import FileService
from backend.storage.models import File


@pytest.fixture
def deletion(db_session, monkeypatch):
    owner = User(email=f"{uuid4().hex}@example.com", username=uuid4().hex)
    owner.roles = [
        db_session.exec(select(Role).where(Role.name == UserRole.EDUCATOR)).one()
    ]
    db_session.add(owner)
    db_session.flush()
    course = Course(name="Mechanics", owner_id=owner.id)
    file = File(owner_id=owner.id, original_name="lecture.pdf", storage_key=uuid4().hex)
    db_session.add_all([course, file])
    db_session.flush()
    note = CourseNote(
        course_id=course.id,
        file_id=file.id,
        title="Lecture",
        resource_type=CourseContentType.LECTURE,
    )
    db_session.add(note)
    db_session.flush()
    block = NoteBlock(course_note_id=note.id, title="Block", content={}, position=0)
    db_session.add(block)
    db_session.commit()
    blob = Mock(delete=AsyncMock())
    vectors = Mock(adelete=AsyncMock(return_value=True))
    stores = Mock()
    stores.get_configuration.return_value = object()
    stores.get_vectorstore.return_value = vectors
    monkeypatch.setattr(module, "CourseVectorStoreService", Mock(return_value=stores))
    service = CourseNoteService(
        db_session, FileService(storage=blob, session=db_session)
    )
    return service, owner, note, block, blob, vectors


@pytest.mark.asyncio
async def test_delete_removes_embeddings_blocks_note_and_file(deletion, db_session):
    service, owner, note, block, blob, vectors = deletion
    note_id, block_id, file_id, key = (
        note.id,
        block.id,
        note.file_id,
        note.file.storage_key,
    )
    await service.delete(note_id, user=owner)
    vectors.adelete.assert_awaited_once_with(ids=[str(block_id)])
    blob.delete.assert_awaited_once_with(key)
    db_session.expunge_all()
    assert db_session.get(CourseNote, note_id) is None
    assert db_session.get(NoteBlock, block_id) is None
    assert db_session.get(File, file_id) is None


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "run_status",
    [ProcessingStatus.PENDING, ProcessingStatus.STARTED, ProcessingStatus.RETRY],
)
async def test_active_processing_prevents_deletion(deletion, db_session, run_status):
    service, owner, note, block, blob, vectors = deletion
    run = ProcessingRun(
        celery_task_id=uuid4(),
        task_type="lecture_processing",
        status=run_status,
        stage=ProcessingStage.INDEXING,
    )
    db_session.add(run)
    db_session.flush()
    db_session.add(LectureProcessingRun(run_id=run.id, note_id=note.id))
    db_session.commit()
    with pytest.raises(CourseNoteDeletionConflictError):
        await service.delete(note.id, user=owner)
    vectors.adelete.assert_not_awaited()
    blob.delete.assert_not_awaited()
    assert db_session.get(NoteBlock, block.id) is not None


@pytest.mark.asyncio
async def test_vector_failure_preserves_source_data(deletion, db_session):
    service, owner, note, block, blob, vectors = deletion
    vectors.adelete.return_value = False
    with pytest.raises(CourseNoteDeletionError):
        await service.delete(note.id, user=owner)
    db_session.expunge_all()
    assert db_session.get(CourseNote, note.id) is not None
    assert db_session.get(NoteBlock, block.id) is not None
    blob.delete.assert_not_awaited()


@pytest.mark.asyncio
async def test_delete_requires_course_ownership(deletion, db_session):
    service, _owner, note, _block, blob, vectors = deletion
    other = User(email=f"{uuid4().hex}@example.com", username=uuid4().hex)
    other.roles = list(
        db_session.exec(select(Role).where(Role.name == UserRole.EDUCATOR)).all()
    )
    db_session.add(other)
    db_session.commit()
    with pytest.raises(CourseOwnershipError):
        await service.delete(note.id, user=other)
    vectors.adelete.assert_not_awaited()
    blob.delete.assert_not_awaited()


@pytest.mark.asyncio
async def test_completed_processing_does_not_prevent_deletion(deletion, db_session):
    service, owner, note, _block, _blob, vectors = deletion
    run = ProcessingRun(
        celery_task_id=uuid4(),
        task_type="lecture_processing",
        status=ProcessingStatus.SUCCESS,
        stage=ProcessingStage.INDEXING,
    )
    db_session.add(run)
    db_session.flush()
    db_session.add(LectureProcessingRun(run_id=run.id, note_id=note.id))
    db_session.commit()
    await service.delete(note.id, user=owner)
    vectors.adelete.assert_awaited_once()


@pytest.mark.asyncio
async def test_shared_file_cannot_delete_another_attachment(deletion, db_session):
    service, owner, note, _block, blob, vectors = deletion
    other_course = Course(name="Other", owner_id=owner.id)
    db_session.add(other_course)
    db_session.flush()
    db_session.add(
        CourseNote(
            course_id=other_course.id,
            file_id=note.file_id,
            title="Shared file",
            resource_type=CourseContentType.LECTURE,
        )
    )
    db_session.commit()
    with pytest.raises(CourseNoteDeletionConflictError):
        await service.delete(note.id, user=owner)
    vectors.adelete.assert_not_awaited()
    blob.delete.assert_not_awaited()


@pytest.mark.asyncio
async def test_vector_exception_preserves_file(deletion, db_session):
    service, owner, note, _block, blob, vectors = deletion
    vectors.adelete.side_effect = TimeoutError("provider unavailable")
    with pytest.raises(CourseNoteDeletionError):
        await service.delete(note.id, user=owner)
    assert db_session.get(File, note.file_id) is not None
    blob.delete.assert_not_awaited()


def test_deletion_errors_have_actionable_http_status():
    from backend.web.courses.http import course_http_exception

    assert (
        course_http_exception(CourseNoteDeletionConflictError("Busy")).status_code
        == 409
    )
    assert (
        course_http_exception(CourseNoteDeletionError("Cleanup failed")).status_code
        == 500
    )

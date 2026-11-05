from datetime import UTC, datetime, timedelta
from uuid import UUID, uuid4

import pytest

from backend.accounts.models import User
from backend.courses.models import Course, CourseContentType, CourseNote
from backend.courses.repo.lecture_processing_repo import LectureProcessingRepository
from backend.processing.models import (
    LectureProcessingRun,
    ProcessingRun,
    ProcessingStage,
    ProcessingStatus,
)
from backend.storage.models import File


@pytest.fixture
def records(db_session):
    owner = User(email=f"{uuid4().hex}@example.com", username=uuid4().hex)
    db_session.add(owner)
    db_session.flush()
    course = Course(name="Mechanics", owner_id=owner.id)
    db_session.add(course)
    db_session.flush()
    notes = []
    for _ in range(2):
        file = File(
            owner_id=owner.id, original_name="lecture.pdf", storage_key=uuid4().hex
        )
        db_session.add(file)
        db_session.flush()
        note = CourseNote(
            course_id=course.id,
            file_id=file.id,
            title="Lecture",
            resource_type=CourseContentType.LECTURE,
        )
        db_session.add(note)
        db_session.flush()
        notes.append(note)

    def add_run(note, status, *, day=0, run_id=None):
        run = ProcessingRun(
            id=run_id or uuid4(),
            celery_task_id=uuid4(),
            task_type="lecture_processing",
            status=status,
            stage=ProcessingStage.INDEXING,
            created_at=datetime(2026, 1, 1, tzinfo=UTC) + timedelta(days=day),
        )
        db_session.add(run)
        db_session.flush()
        db_session.add(LectureProcessingRun(run_id=run.id, note_id=note.id))
        db_session.flush()
        return run

    return LectureProcessingRepository(db_session), notes, add_run


def test_run_lookup_is_scoped_to_note(records):
    repo, (note, other), add = records
    run = add(note, ProcessingStatus.SUCCESS)
    assert repo.get_by_note_and_run(note.id, run.id).id == run.id
    assert repo.get_by_note_and_run(other.id, run.id) is None
    assert repo.get_by_note_and_run(note.id, uuid4()) is None


def test_list_orders_limits_and_excludes_other_notes(records):
    repo, (note, other), add = records
    oldest = add(note, ProcessingStatus.SUCCESS)
    newest = add(note, ProcessingStatus.FAILURE, day=1)
    add(other, ProcessingStatus.SUCCESS, day=2)
    assert [r.id for r in repo.list_by_note(note.id)] == [newest.id, oldest.id]
    assert [r.id for r in repo.list_by_note(note.id, order="oldest", limit=1)] == [
        oldest.id
    ]
    assert repo.get_latest(note.id).id == newest.id


def test_filter_is_applied_before_limit(records):
    repo, (note, _), add = records
    successful = add(note, ProcessingStatus.SUCCESS)
    active = add(note, ProcessingStatus.RETRY, day=1)
    add(note, ProcessingStatus.FAILURE, day=2)
    assert repo.get_latest_successful(note.id).id == successful.id
    assert repo.get_latest_active(note.id).id == active.id
    assert list(repo.list_by_note(note.id, statuses=[])) == []


def test_equal_timestamps_have_stable_id_order(records):
    repo, (note, _), add = records
    low = add(note, ProcessingStatus.STARTED, run_id=UUID(int=1))
    high = add(note, ProcessingStatus.STARTED, run_id=UUID(int=2))
    assert [r.id for r in repo.list_by_note(note.id)] == [high.id, low.id]
    assert [r.id for r in repo.list_by_note(note.id, order="oldest")] == [
        low.id,
        high.id,
    ]
    assert repo.get_latest_active(note.id).id == high.id


@pytest.mark.parametrize(
    "method", ["get_latest", "get_latest_active", "get_latest_successful"]
)
def test_no_matching_run_returns_none(records, method):
    repo, (note, _), _add = records
    assert getattr(repo, method)(note.id) is None


@pytest.mark.parametrize("limit", [0, -1])
def test_invalid_limit_is_rejected(records, limit):
    repo, (note, _), _add = records
    with pytest.raises(ValueError, match="Limit"):
        repo.list_by_note(note.id, limit=limit)


def test_invalid_order_is_rejected(records):
    repo, (note, _), _add = records
    with pytest.raises(ValueError, match="Unsupported order"):
        repo.list_by_note(note.id, order="invalid")

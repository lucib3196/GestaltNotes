from uuid import uuid4

import pytest
from sqlmodel import Session, SQLModel, create_engine

import backend.accounts.models  # noqa: F401 -- Register relationship targets.
from backend.courses.models import Course, CourseContentType, CourseNote
from backend.processing.exceptions import (
    LectureAlreadyProcessedError,
    LectureProcessingNoteNotFoundError,
    LectureProcessingRunNotFoundError,
)
from backend.processing.lecture_processing_service import LectureProcessingService
from backend.processing.models import (
    LectureProcessingRun,
    ProcessingRun,
    ProcessingStage,
    ProcessingStatus,
)
from backend.storage.models import File


@pytest.fixture
def records():
    engine = create_engine("sqlite://")
    SQLModel.metadata.create_all(
        engine,
        tables=[
            Course.__table__,
            File.__table__,
            CourseNote.__table__,
            ProcessingRun.__table__,
            LectureProcessingRun.__table__,
        ],
    )
    with Session(engine) as session:
        course = Course(name="Calculus", discipline="Math", owner_id=uuid4())
        session.add(course)
        session.flush()
        file = File(
            owner_id=course.owner_id,
            original_name="lecture.pdf",
            storage_key="lecture.pdf",
        )
        session.add(file)
        session.flush()
        note = CourseNote(
            course_id=course.id,
            file_id=file.id,
            title="Lecture",
            resource_type=CourseContentType.LECTURE,
        )
        session.add(note)
        session.commit()
        yield session, course, note
    engine.dispose()


def add_run(session, note_id, status):
    run = ProcessingRun(
        celery_task_id=uuid4(),
        task_type="lecture_processing",
        status=status,
        stage=ProcessingStage.INDEXING,
    )
    session.add(run)
    session.flush()
    session.add(LectureProcessingRun(run_id=run.id, note_id=note_id))
    session.commit()
    return run


@pytest.mark.parametrize(
    "status",
    [None, ProcessingStatus.FAILED, ProcessingStatus.PARTIAL, ProcessingStatus.RUNNING],
)
def test_non_successful_run_allows_processing(records, status):
    session, course, note = records
    add_run(session, note.id, status)
    assert (
        LectureProcessingService(session).assert_can_process(course.id, note.id).id
        == note.id
    )


def test_any_successful_run_blocks_reprocessing(records):
    session, course, note = records
    add_run(session, note.id, ProcessingStatus.SUCCEEDED)
    add_run(session, note.id, ProcessingStatus.FAILED)
    service = LectureProcessingService(session)
    with pytest.raises(LectureAlreadyProcessedError):
        service.assert_can_process(course.id, note.id)


def test_success_for_different_note_does_not_block(records):
    session, course, note = records
    add_run(session, uuid4(), ProcessingStatus.SUCCEEDED)
    assert (
        LectureProcessingService(session).assert_can_process(course.id, note.id).id
        == note.id
    )


def test_retrieval_is_scoped_to_note_and_course(records):
    session, course, note = records
    run = add_run(session, note.id, ProcessingStatus.FAILED)
    unrelated = add_run(session, uuid4(), ProcessingStatus.SUCCEEDED)
    service = LectureProcessingService(session)
    assert [item.id for item in service.list_runs(course.id, note.id)] == [run.id]
    assert service.get_run(course.id, note.id, run.id).id == run.id
    with pytest.raises(LectureProcessingRunNotFoundError):
        service.get_run(course.id, note.id, unrelated.id)
    with pytest.raises(LectureProcessingRunNotFoundError):
        service.get_run(course.id, note.id, uuid4())
    with pytest.raises(LectureProcessingNoteNotFoundError):
        service.list_runs(uuid4(), note.id)
    with pytest.raises(LectureProcessingNoteNotFoundError):
        service.assert_can_process(course.id, uuid4())


@pytest.mark.asyncio
@pytest.mark.parametrize("successful", [True, False])
async def test_dispatch_rejects_success_without_queuing(
    records, monkeypatch, successful
):
    from types import SimpleNamespace
    from unittest.mock import Mock

    from fastapi import HTTPException

    from backend.web.processing.tasks import (
        process_lecture_file,
        start_lecture_processing,
    )

    session, course, note = records
    add_run(
        session,
        note.id,
        ProcessingStatus.SUCCEEDED if successful else ProcessingStatus.FAILED,
    )
    submit = Mock(return_value=SimpleNamespace(id="queued-task"))
    monkeypatch.setattr(process_lecture_file, "apply_async", submit)
    if successful:
        with pytest.raises(HTTPException) as caught:
            await start_lecture_processing(course.id, note.id, session, course)
        assert caught.value.status_code == 409
        submit.assert_not_called()
    else:
        response = await start_lecture_processing(course.id, note.id, session, course)
        assert response["task_id"] == "queued-task"
        assert submit.call_args.kwargs["args"] == [
            {"course_id": str(course.id), "note_id": str(note.id)}
        ]


def test_preparation_rechecks_success_before_creating_run(records, monkeypatch):
    from contextlib import contextmanager
    from unittest.mock import Mock

    from backend.processing import tasks
    from backend.processing.schema import LectureProcessingInput

    session, course, note = records
    add_run(session, note.id, ProcessingStatus.SUCCEEDED)

    @contextmanager
    def session_scope():
        yield session

    monkeypatch.setattr(tasks, "open_session", session_scope)
    note_scope = Mock()
    monkeypatch.setattr(tasks, "course_note_scope", note_scope)
    payload = LectureProcessingInput(course_id=course.id, note_id=note.id)
    with pytest.raises(LectureAlreadyProcessedError):
        tasks.prepare_lecture_run.run(payload.model_dump(mode="json"))
    note_scope.assert_not_called()
    assert len(LectureProcessingService(session).list_runs(course.id, note.id)) == 1

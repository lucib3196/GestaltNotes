from datetime import UTC
from uuid import uuid4

import pytest
from sqlmodel import Session, SQLModel, create_engine

import backend.accounts.models  # noqa: F401 -- Register relationship targets.
from backend.courses.exceptions import CourseNoteNotFoundError
from backend.courses.models import Course, CourseContentType, CourseNote
from backend.courses.service.course_note_processing_service import (
    CourseNoteProcessingService,
)
from backend.processing.exceptions import (
    LectureAlreadyProcessedError,
    LectureProcessingInProgressError,
    LectureProcessingRunNotFoundError,
)
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
            content_type="application/pdf",
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
    [
        ProcessingStatus.FAILURE,
        ProcessingStatus.REVOKED,
    ],
)
@pytest.mark.asyncio
async def test_non_successful_run_allows_processing(records, status):
    session, _course, note = records
    add_run(session, note.id, status)
    assert (
        await CourseNoteProcessingService(session).assert_can_process(note.id)
    ).id == note.id


@pytest.mark.asyncio
async def test_any_successful_run_blocks_reprocessing(records):
    session, _course, note = records
    add_run(session, note.id, ProcessingStatus.SUCCESS)
    add_run(session, note.id, ProcessingStatus.FAILURE)
    service = CourseNoteProcessingService(session)
    with pytest.raises(LectureAlreadyProcessedError):
        await service.assert_can_process(note.id)


@pytest.mark.asyncio
async def test_success_for_different_note_does_not_block(records):
    session, _course, note = records
    add_run(session, uuid4(), ProcessingStatus.SUCCESS)
    assert (
        await CourseNoteProcessingService(session).assert_can_process(note.id)
    ).id == note.id


@pytest.mark.asyncio
async def test_retrieval_is_scoped_to_note(records):
    session, _course, note = records
    run = add_run(session, note.id, ProcessingStatus.FAILURE)
    unrelated = add_run(session, uuid4(), ProcessingStatus.SUCCESS)
    service = CourseNoteProcessingService(session)
    assert [item.id for item in await service.list_runs(note.id)] == [run.id]
    assert (await service.get_run(note.id, run.id)).id == run.id
    with pytest.raises(LectureProcessingRunNotFoundError):
        await service.get_run(note.id, unrelated.id)
    with pytest.raises(LectureProcessingRunNotFoundError):
        await service.get_run(note.id, uuid4())
    with pytest.raises(CourseNoteNotFoundError):
        await service.list_runs(uuid4())
    with pytest.raises(CourseNoteNotFoundError):
        await service.assert_can_process(uuid4())


@pytest.mark.asyncio
@pytest.mark.parametrize("successful", [True, False])
async def test_dispatch_rejects_success_without_queuing(
    records, monkeypatch, successful
):
    from types import SimpleNamespace
    from unittest.mock import Mock

    from fastapi import HTTPException

    from backend.web.courses.processing_runs import (
        process_lecture_file,
        start_lecture_processing,
    )

    session, course, note = records
    add_run(
        session,
        note.id,
        ProcessingStatus.SUCCESS if successful else ProcessingStatus.FAILURE,
    )
    submit = Mock(return_value=SimpleNamespace(id="queued-task"))
    monkeypatch.setattr(process_lecture_file, "apply_async", submit)
    if successful:
        with pytest.raises(HTTPException) as caught:
            await start_lecture_processing(
                course.id, note.id, CourseNoteProcessingService(session), note
            )
        assert caught.value.status_code == 409
        submit.assert_not_called()
    else:
        response = await start_lecture_processing(
            course.id, note.id, CourseNoteProcessingService(session), note
        )
        assert response["task_id"] == "queued-task"
        assert submit.call_args.kwargs["args"] == [
            {
                "course_id": str(course.id),
                "note_id": str(note.id),
                "file_id": str(note.file_id),
            }
        ]


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "run_status",
    [
        ProcessingStatus.PENDING,
        ProcessingStatus.RECEIVED,
        ProcessingStatus.STARTED,
        ProcessingStatus.PROGRESS,
        ProcessingStatus.RETRY,
    ],
)
async def test_active_run_blocks_dispatch(records, monkeypatch, run_status):
    from unittest.mock import Mock

    from fastapi import HTTPException

    from backend.web.courses import processing_runs

    session, course, note = records
    add_run(session, note.id, run_status)
    submit = Mock()
    monkeypatch.setattr(processing_runs.process_lecture_file, "apply_async", submit)
    service = CourseNoteProcessingService(session)
    with pytest.raises(LectureProcessingInProgressError):
        await service.assert_can_process(note.id)
    with pytest.raises(HTTPException) as caught:
        await processing_runs.start_lecture_processing(
            course.id, note.id, service, note
        )
    assert caught.value.status_code == 409
    submit.assert_not_called()
    assert not (await service.get_processing_status(note.id)).can_process


@pytest.mark.asyncio
async def test_status_before_processing(records):
    session, _, note = records
    summary = await CourseNoteProcessingService(session).get_processing_status(note.id)
    assert summary.has_succeeded is False
    assert summary.can_process is True
    assert summary.latest_run is None


@pytest.mark.asyncio
async def test_status_preserves_success_when_latest_run_failed(records):
    from datetime import datetime, timedelta

    session, _, note = records
    succeeded = add_run(session, note.id, ProcessingStatus.SUCCESS)
    failed = add_run(session, note.id, ProcessingStatus.FAILURE)
    succeeded.created_at = datetime.now(UTC) - timedelta(minutes=1)
    failed.created_at = datetime.now(UTC)
    session.commit()

    summary = await CourseNoteProcessingService(session).get_processing_status(note.id)
    assert summary.has_succeeded is True
    assert summary.can_process is False
    assert summary.latest_run.id == failed.id
    assert summary.latest_run.status == ProcessingStatus.FAILURE


@pytest.mark.asyncio
async def test_course_note_dependency_rejects_note_from_other_course(records):
    from fastapi import HTTPException

    from backend.web.courses.dependencies import get_readable_course_note

    session, course, note = records
    other_course = Course(name="Other", owner_id=course.owner_id)
    session.add(other_course)
    session.commit()

    assert await get_readable_course_note(note.id, course, session) is note
    with pytest.raises(HTTPException) as caught:
        await get_readable_course_note(note.id, other_course, session)
    assert caught.value.status_code == 404


@pytest.mark.asyncio
async def test_overviews_are_scoped_to_course(records):
    session, course, note = records
    add_run(session, note.id, ProcessingStatus.SUCCESS)
    service = CourseNoteProcessingService(session)
    overviews = await service.list_notes_overview(course.id)
    assert [overview.id for overview in overviews] == [note.id]
    assert overviews[0].processing.has_succeeded is True
    assert await service.list_notes_overview(uuid4()) == []


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "run_status", [ProcessingStatus.STARTED, ProcessingStatus.FAILURE]
)
async def test_scoped_status_exposes_stage_and_failure(records, run_status):
    from backend.processing.models import LectureProcessingStatusRead
    from backend.web.courses.processing_runs import get_processing_status

    session, _course, note = records
    run = add_run(session, note.id, run_status)
    run.stage = ProcessingStage.EXTRACTING
    if run_status == ProcessingStatus.FAILURE:
        run.error_type = "RuntimeError"
        run.error_message = "Processing failed during extracting"
    session.add(run)
    session.commit()

    response = await get_processing_status(
        note.id, CourseNoteProcessingService(session), note
    )
    payload = LectureProcessingStatusRead.model_validate(response)
    assert payload.latest_run is not None
    assert payload.latest_run.celery_task_id == run.celery_task_id
    assert payload.latest_run.status == run_status
    assert payload.latest_run.stage == ProcessingStage.EXTRACTING
    assert payload.latest_run.error_message == run.error_message
    assert not payload.has_succeeded

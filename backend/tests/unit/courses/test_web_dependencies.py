from types import SimpleNamespace
from unittest.mock import AsyncMock, Mock
from uuid import uuid4

import pytest
from fastapi import FastAPI, HTTPException
from fastapi.routing import APIRoute
from pydantic import ValidationError

from backend.accounts.models import User, UserRole
from backend.courses.models import (
    Course,
    CourseContentType,
    CourseNote,
    CourseNoteUpdate,
)
from backend.courses.service.course_note_service import CourseNoteService
from backend.web.accounts.dependencies import get_current_user
from backend.web.courses import course_routes
from backend.web.courses.dependencies import (
    get_owned_course,
    get_owned_course_note,
    get_readable_course,
    get_readable_course_note,
)
from backend.web.courses.notes import get_note_overview, update_course_note
from backend.web.courses.processing_runs import start_lecture_processing


@pytest.mark.parametrize(
    ("owner", "active", "expected"),
    [
        (True, None, 200),
        (False, True, 200),
        (False, False, 403),
        (False, None, 403),
    ],
)
def test_read_access(owner, active, expected):
    user = User(email="reader@example.com")
    course = Course(name="Course", owner_id=user.id if owner else uuid4())
    session = Mock()
    enrollment = SimpleNamespace(active=active) if active is not None else None
    session.get.side_effect = [course, enrollment]
    if expected == 200:
        assert get_readable_course(course.id, session, user) is course
    else:
        with pytest.raises(HTTPException) as exc:
            get_readable_course(course.id, session, user)
        assert exc.value.status_code == expected


@pytest.mark.parametrize("owned", [False, True])
async def test_note_dependencies_scope_the_query(monkeypatch, owned):
    from backend.web.courses import dependencies

    session = Mock()
    course = Course(name="Course", owner_id=uuid4())
    note_id = uuid4()
    repository = SimpleNamespace(get_by_course_and_note=AsyncMock(return_value=None))
    monkeypatch.setattr(dependencies, "CourseNoteRepository", lambda _: repository)
    dependency = get_owned_course_note if owned else get_readable_course_note
    with pytest.raises(HTTPException) as exc:
        await dependency(note_id, course, session)
    assert exc.value.status_code == 404
    repository.get_by_course_and_note.assert_awaited_once_with(course.id, note_id)


@pytest.mark.parametrize(
    ("role", "is_owner", "expected"),
    [
        (UserRole.EDUCATOR, True, 200),
        (UserRole.EDUCATOR, False, 403),
        (UserRole.STUDENT, True, 403),
    ],
)
async def test_owned_course_requires_educator_and_ownership(
    monkeypatch, role, is_owner, expected
):
    from backend.web.courses import dependencies

    user = SimpleNamespace(id=uuid4(), roles=[SimpleNamespace(name=role)])
    course = Course(name="Course", owner_id=user.id if is_owner else uuid4())
    repository = SimpleNamespace(get=AsyncMock(return_value=course))
    monkeypatch.setattr(dependencies, "CourseRepo", lambda _: repository)
    if expected == 200:
        assert await get_owned_course(course.id, Mock(), user) is course
    else:
        with pytest.raises(HTTPException) as exc:
            await get_owned_course(course.id, Mock(), user)
        assert exc.value.status_code == expected


def dependency_calls(dependant):
    calls = {dependant.call}
    for child in dependant.dependencies:
        calls.update(dependency_calls(child))
    return calls


def test_route_permissions_and_registration():
    app = FastAPI()
    for router in course_routes:
        app.include_router(router)
    routes = {
        route.endpoint.__name__: route
        for route in app.routes
        if isinstance(route, APIRoute)
    }
    assert get_current_user in dependency_calls(routes["get_course"].dependant)
    assert get_readable_course in dependency_calls(routes["get_course"].dependant)
    for name in [
        "start_lecture_processing",
        "update_course_note",
        "remove_course_note",
    ]:
        assert get_owned_course_note in dependency_calls(routes[name].dependant)
    assert get_readable_course_note in dependency_calls(
        routes["get_note_overview"].dependant
    )
    assert not any("access-codes" in path for path in app.openapi()["paths"])


@pytest.mark.parametrize("field", ["title", "resource_type"])
def test_explicit_null_update_rejected(field):
    with pytest.raises(ValidationError):
        CourseNoteUpdate.model_validate({field: None})
    assert CourseNoteUpdate().model_dump(exclude_unset=True) == {}


async def test_note_overview_allows_read_dependency_without_owner_check():
    processing = SimpleNamespace(get_note_overview=AsyncMock(return_value=Mock()))
    note_id = uuid4()
    result = await get_note_overview(note_id, processing, Mock())
    assert result is processing.get_note_overview.return_value
    processing.get_note_overview.assert_awaited_once_with(note_id)


async def test_update_passes_authenticated_actor():
    service = AsyncMock(spec=CourseNoteService)
    service.to_note_read = Mock()
    note_id = uuid4()
    educator = Mock()
    update = CourseNoteUpdate(title="Updated")
    await update_course_note(note_id, educator, service, Mock(), update)
    service.update.assert_awaited_once_with(note_id, update, user=educator)


async def test_processing_uses_validated_note_and_course(monkeypatch):
    from backend.storage.models import File
    from backend.web.courses import processing_runs

    note = CourseNote(
        course_id=uuid4(),
        file_id=uuid4(),
        title="Note",
        resource_type=CourseContentType.NOTES,
    )
    note.file = File(
        id=note.file_id,
        owner_id=uuid4(),
        original_name="lecture.pdf",
        storage_key="lecture.pdf",
        content_type="application/pdf",
    )
    task = Mock(return_value=SimpleNamespace(id="task-id"))
    monkeypatch.setattr(processing_runs.process_lecture_file, "apply_async", task)
    service = SimpleNamespace(assert_can_process=AsyncMock())
    result = await start_lecture_processing(note.course_id, note.id, service, note)
    assert result["task_id"] == "task-id"
    task.assert_called_once_with(
        args=[
            {
                "course_id": str(note.course_id),
                "note_id": str(note.id),
                "file_id": str(note.file_id),
            }
        ]
    )


def test_block_reads_do_not_construct_indexing_and_mutations_are_scoped():
    from backend.web.courses import dependencies

    app = FastAPI()
    for router in course_routes:
        app.include_router(router)
    routes = {
        route.endpoint.__name__: route
        for route in app.routes
        if isinstance(route, APIRoute)
    }
    for name in ("list_note_blocks", "get_note_block"):
        calls = dependency_calls(routes[name].dependant)
        assert dependencies.get_readable_course in calls
        assert dependencies.get_note_block_service not in calls
    for name in ("update_note_block", "delete_note_block", "reindex_note_block"):
        calls = dependency_calls(routes[name].dependant)
        assert dependencies.get_owned_note_block in calls
        assert dependencies.get_owned_course in calls
    schema = app.openapi()["paths"]
    path = "/courses/notes/{course_id}/{note_id}"
    assert "get" in schema[path]
    assert schema[path]["put"]["deprecated"] is True
    assert "patch" in schema[path]


@pytest.mark.parametrize(
    "wrong_course,active,expected",
    [
        (True, False, 404),
        (False, True, 409),
        (False, False, 200),
    ],
)
async def test_block_mutation_scope_and_active_processing(
    monkeypatch, wrong_course, active, expected
):
    from backend.web.courses import dependencies

    course = SimpleNamespace(id=uuid4())
    block = SimpleNamespace(
        id=uuid4(),
        course_note_id=uuid4(),
        course_note=SimpleNamespace(course_id=uuid4() if wrong_course else course.id),
    )
    repo = SimpleNamespace(get=AsyncMock(return_value=block))
    runs = SimpleNamespace(
        get_latest_active=Mock(return_value=object() if active else None)
    )
    monkeypatch.setattr(dependencies, "NoteBlockRepo", lambda _: repo)
    monkeypatch.setattr(dependencies, "LectureProcessingRepository", lambda _: runs)
    if expected == 200:
        assert (
            await dependencies.get_owned_note_block(block.id, course, Mock()) is block
        )
    else:
        with pytest.raises(HTTPException) as exc:
            await dependencies.get_owned_note_block(block.id, course, Mock())
        assert exc.value.status_code == expected
    if wrong_course:
        runs.get_latest_active.assert_not_called()


async def test_processing_history_forwards_filters():
    from backend.processing.models import ProcessingStatus
    from backend.web.courses.processing_runs import list_processing_runs

    service = SimpleNamespace(list_runs=AsyncMock(return_value=[]))
    note_id = uuid4()
    statuses = [ProcessingStatus.FAILURE]
    assert (
        await list_processing_runs(
            note_id, service, Mock(), order="oldest", limit=5, statuses=statuses
        )
        == []
    )
    service.list_runs.assert_awaited_once_with(
        note_id, order="oldest", limit=5, statuses=statuses
    )


async def test_block_mutations_delegate_to_indexing_service():
    from backend.courses.models import NoteBlockUpdate
    from backend.web.courses.note_blocks import (
        delete_note_block,
        reindex_note_block,
        update_note_block,
    )

    block = SimpleNamespace(id=uuid4())
    service = SimpleNamespace(
        update=AsyncMock(return_value=block),
        delete=AsyncMock(),
        reindex=AsyncMock(),
    )
    update = NoteBlockUpdate(title="Updated")
    assert await update_note_block(update, block, service) is block
    service.update.assert_awaited_once_with(block.id, update)
    assert (await reindex_note_block(block, service, True)).status_code == 204
    service.reindex.assert_awaited_once_with(block.id, force_recreate=True)
    assert (await delete_note_block(block, service)).status_code == 204
    service.delete.assert_awaited_once_with(block.id)


async def test_block_validation_error_returns_422():
    from backend.courses.exceptions import NoteBlockValidationError
    from backend.courses.models import NoteBlockUpdate
    from backend.web.courses.note_blocks import update_note_block

    block = SimpleNamespace(id=uuid4())
    service = SimpleNamespace(
        update=AsyncMock(side_effect=NoteBlockValidationError("Invalid content"))
    )
    with pytest.raises(HTTPException) as exc:
        await update_note_block(NoteBlockUpdate(), block, service)
    assert exc.value.status_code == 422


def test_composed_services_share_repository_and_session():
    from backend.web.courses import dependencies

    session = Mock()
    repo = Mock()
    store = Mock()
    indexer = dependencies.get_indexer(store, repo)
    factory = Mock(return_value=indexer)
    blocks = dependencies.get_note_block_service(session, repo, factory)
    factory.assert_not_called()
    assert blocks._get_indexer() is indexer
    assert blocks._get_indexer() is indexer
    factory.assert_called_once_with()
    notes = Mock()
    files = Mock()
    access = Mock()
    service = dependencies.get_course_note_service(
        session, files, notes, blocks, access
    )

    assert indexer._repo is repo
    assert indexer._store is store
    assert blocks._session is session
    assert blocks._blocks is repo
    assert blocks._indexer is indexer
    assert service._session is session
    assert service._blocks is blocks
    assert service._notes is notes
    assert service._files is files
    assert service._access is access


def test_vectorstore_dependency_selects_authorized_course():
    from backend.web.courses import dependencies

    course = SimpleNamespace(id=uuid4())
    stores = Mock()
    assert (
        dependencies.get_course_vectorstore(course, stores)
        is stores.get_vectorstore.return_value
    )
    stores.get_vectorstore.assert_called_once_with(course.id, async_mode=True)


def test_vectorstore_dependency_reports_unavailable_configuration():
    from backend.web.courses import dependencies

    course = SimpleNamespace(id=uuid4())
    stores = Mock()
    stores.get_vectorstore.side_effect = LookupError("Not configured")
    with pytest.raises(HTTPException) as exc:
        dependencies.get_course_vectorstore(course, stores)
    assert exc.value.status_code == 503


async def test_upload_does_not_initialize_unconfigured_vectorstore():
    from tempfile import SpooledTemporaryFile

    from fastapi import UploadFile

    from backend.courses.repo.course_notes_repo import CourseNoteRepository
    from backend.storage.models import File
    from backend.web.courses import dependencies
    from backend.web.courses.notes import router, upload_course_note

    course = Course(name="Mechanics", owner_id=uuid4())
    owner = SimpleNamespace(id=course.owner_id)
    stores = Mock()
    stores.get_vectorstore.side_effect = LookupError("Not configured")
    session = Mock()
    notes = CourseNoteRepository(session)
    notes.create = AsyncMock(side_effect=lambda note: note)
    file = File(
        owner_id=owner.id,
        original_name="note.md",
        storage_key="notes/note.md",
        content_type="text/markdown",
    )
    files = SimpleNamespace(stage_file=AsyncMock(return_value=file))
    access = SimpleNamespace(require_owner=AsyncMock(return_value=course))
    factory = dependencies.get_indexer_factory(course, stores, Mock())
    blocks = dependencies.get_note_block_service(session, Mock(), factory)
    service = dependencies.get_course_note_service(
        session, files, notes, blocks, access
    )
    with SpooledTemporaryFile() as upload_data:
        upload_data.write(b"# Lecture")
        upload_data.seek(0)
        upload = UploadFile(filename="note.md", file=upload_data)
        result = await upload_course_note(
            course.id, owner, service, upload, CourseContentType.NOTES
        )

    assert result.course_id == course.id
    stores.get_vectorstore.assert_not_called()
    files.stage_file.assert_awaited_once()
    session.commit.assert_called_once_with()

    # Verify FastAPI uses the deferred factory rather than the eager store.
    route = next(
        route
        for route in router.routes
        if isinstance(route, APIRoute) and route.endpoint is upload_course_note
    )
    calls = dependency_calls(route.dependant)
    assert dependencies.get_indexer_factory in calls
    assert dependencies.get_course_vectorstore not in calls


async def test_lazy_indexer_reports_configuration_failure_when_used():
    from backend.web.courses import dependencies

    course = SimpleNamespace(id=uuid4())
    stores = Mock()
    stores.get_vectorstore.side_effect = LookupError("Not configured")
    repo = SimpleNamespace(get=AsyncMock(return_value=Mock()))
    factory = dependencies.get_indexer_factory(course, stores, repo)
    service = dependencies.get_note_block_service(Mock(), repo, factory)
    stores.get_vectorstore.assert_not_called()

    with pytest.raises(HTTPException) as exc:
        await service.reindex(uuid4())

    assert exc.value.status_code == 503
    stores.get_vectorstore.assert_called_once_with(course.id, async_mode=True)

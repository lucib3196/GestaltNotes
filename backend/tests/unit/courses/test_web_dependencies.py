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
    service.update_note_properties.assert_awaited_once_with(
        note_id, update, user=educator
    )


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

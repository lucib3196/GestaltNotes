from uuid import uuid4

import pytest
import pytest_asyncio

from backend.courses.models import CourseContentType, CourseNote
from backend.storage.models import File


@pytest_asyncio.fixture
async def course_owner(make_user):
    suffix = uuid4().hex
    user = {
        "email": f"course-note-owner-{suffix}@example.com",
        "username": f"course-note-owner-{suffix}",
    }

    return await make_user(role="educator", **user)


@pytest_asyncio.fixture
async def course(make_course, course_owner):
    return await make_course(course_owner)


@pytest.fixture
def file_record(db_session, course_owner):
    assert course_owner.id is not None
    file = File(
        owner_id=course_owner.id,
        original_name="lecture-note.pdf",
        storage_key=f"tests/course-notes/{uuid4().hex}/lecture-note.pdf",
        content_type="application/pdf",
        size_bytes=128,
    )
    db_session.add(file)
    db_session.commit()
    db_session.refresh(file)
    return file


@pytest.mark.asyncio
async def test_add_file_to_course_creates_course_note(
    course_note_service,
    db_session,
    course,
    file_record,
):
    note = await course_note_service.add_file_to_course(
        course,
        file_record,
        resource_type=CourseContentType.LECTURE,
        title="Lecture 1",
    )

    assert note.id is not None
    assert note.course_id == course.id
    assert note.file_id == file_record.id
    assert note.title == "Lecture 1"
    assert note.resource_type == CourseContentType.LECTURE

    persisted = db_session.get(CourseNote, note.id)
    assert persisted is not None
    assert persisted.course_id == course.id
    assert persisted.file_id == file_record.id


@pytest.mark.asyncio
async def test_add_file_to_course_uses_file_name_as_default_title(
    course_note_service,
    course,
    file_record,
):
    note = await course_note_service.add_file_to_course(course, file_record)

    assert note.title == "lecture-note.pdf"
    assert note.resource_type == CourseContentType.OTHER


@pytest.mark.asyncio
async def test_list_course_notes_returns_notes_for_course(
    course_note_service,
    course,
    file_record,
):
    note = await course_note_service.add_file_to_course(course, file_record)

    notes = await course_note_service.list_course_notes(course.id)

    assert [course_note.id for course_note in notes] == [note.id]


@pytest.mark.asyncio
async def test_remove_file_from_course_deletes_association_only(
    course_note_service,
    db_session,
    course,
    file_record,
):
    note = await course_note_service.add_file_to_course(course, file_record)
    assert note.id is not None
    assert course.id is not None
    assert file_record.id is not None

    await course_note_service.remove_file_from_course(course.id, file_record.id)

    assert db_session.get(CourseNote, note.id) is None
    assert db_session.get(File, file_record.id) is not None

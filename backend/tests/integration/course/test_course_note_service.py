from io import BytesIO
from uuid import uuid4

import pytest
import pytest_asyncio
from fastapi import UploadFile

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
async def course(course_owner, make_course):
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


def upload_file(
    filename: str = "note.md",
    content: bytes = b"# Title\ncontent",
    content_type: str = "text/markdown",
) -> UploadFile:
    return UploadFile(
        file=BytesIO(content),
        filename=filename,
        headers={"content-type": content_type}, # type: ignore
    )


@pytest.mark.asyncio
async def test_add_file_creates_course_note(
    course_note_service,
    db_session,
    course,
    file_record,
):
    note = await course_note_service.add_file(
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
async def test_add_file_uses_file_name_as_default_title(
    course_note_service,
    course,
    file_record,
):
    note = await course_note_service.add_file(course, file_record)

    assert note.title == "lecture-note.pdf"
    assert note.resource_type == CourseContentType.OTHER


@pytest.mark.asyncio
async def test_upload_note_creates_file_and_course_note(
    course_note_service,
    db_session,
    course,
    course_owner,
):
    assert course.id is not None

    note = await course_note_service.upload_note(
        course_id=course.id,
        educator=course_owner,
        upload=upload_file(),
        resource_type=CourseContentType.NOTES,
        title="Uploaded Note",
    )

    assert note.id is not None
    assert note.course_id == course.id
    assert note.title == "Uploaded Note"
    assert note.resource_type == CourseContentType.NOTES

    file = db_session.get(File, note.file_id)
    assert file is not None
    assert file.owner_id == course_owner.id
    assert file.original_name == "note.md"
    assert file.storage_key == f"{course.storage_prefix}/notes/note.md"
    assert file.content_type == "text/markdown"
    assert file.size_bytes == len(b"# Title\ncontent")


@pytest.mark.asyncio
async def test_list_notes_returns_notes_for_course(
    course_note_service,
    course,
    file_record,
):
    note = await course_note_service.add_file(course, file_record)

    notes = await course_note_service.list_notes(course.id)

    assert [course_note.id for course_note in notes] == [note.id]


@pytest.mark.asyncio
async def test_remove_file_deletes_association_only(
    course_note_service,
    db_session,
    course,
    file_record,
):
    note = await course_note_service.add_file(course, file_record)
    assert note.id is not None
    assert course.id is not None
    assert file_record.id is not None

    await course_note_service.remove_file(course.id, file_record.id)

    assert db_session.get(CourseNote, note.id) is None
    assert db_session.get(File, file_record.id) is not None


@pytest.mark.asyncio
async def test_remove_note_deletes_association_file_record_and_blob(
    course_note_service,
    db_session,
    course,
    file_record,
    course_owner,
):
    note = await course_note_service.add_file(course, file_record)
    assert note.id is not None
    assert course.id is not None
    assert file_record.id is not None

    await course_note_service.remove_note(course.id, note.id, course_owner)

    assert db_session.get(CourseNote, note.id) is None
    assert db_session.get(File, file_record.id) is None

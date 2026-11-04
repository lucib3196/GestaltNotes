from uuid import uuid4

import pytest

from backend.accounts.models import User
from backend.courses.models import (
    Course,
    CourseContentType,
    CourseNote,
    NoteBlock,
    NoteBlockUpdate,
)
from backend.courses.repo import NoteBlockRepo
from backend.storage.models import File


@pytest.fixture
def note_block_repo(db_session):
    return NoteBlockRepo(db_session)


@pytest.fixture
def course_note(db_session):
    owner = User(
        email=f"{uuid4().hex}@example.com",
        username=f"owner-{uuid4().hex}",
    )
    db_session.add(owner)
    db_session.flush()
    course = Course(name="Mechanics", owner_id=owner.id)
    file = File(
        owner_id=owner.id,
        original_name="lecture.pdf",
        storage_key=f"tests/{uuid4().hex}/lecture.pdf",
    )
    db_session.add_all([course, file])
    db_session.flush()
    note = CourseNote(
        course_id=course.id,
        file_id=file.id,
        title="Lecture",
        resource_type=CourseContentType.LECTURE,
    )
    db_session.add(note)
    db_session.commit()
    return note


@pytest.fixture
def block(course_note):
    return NoteBlock(
        course_note_id=course_note.id,
        title="Original title",
        kind="lecture_summary",
        content={"text": "Original content"},
        position=0,
    )


@pytest.mark.asyncio
async def test_create_and_get(note_block_repo, db_session, block):
    saved = await note_block_repo.create(block)
    block_id = saved.id
    db_session.expunge_all()
    found = await note_block_repo.get(block_id)
    assert found is not None
    assert found.title == "Original title"
    assert found.content == {"text": "Original content"}
    assert found.course_note_id == block.course_note_id


@pytest.mark.asyncio
async def test_get_missing_block_returns_none(note_block_repo):
    assert await note_block_repo.get(uuid4()) is None


@pytest.mark.asyncio
async def test_update_preserves_omitted_fields(note_block_repo, db_session, block):
    await note_block_repo.create(block)
    block_id = block.id
    await note_block_repo.update(block, NoteBlockUpdate(title="Updated title"))
    db_session.expunge_all()
    found = await note_block_repo.get(block_id)
    assert found is not None
    assert found.title == "Updated title"
    assert found.content == {"text": "Original content"}


@pytest.mark.asyncio
async def test_delete_removes_block(note_block_repo, block):
    await note_block_repo.create(block)
    await note_block_repo.delete(block.id)
    assert await note_block_repo.get(block.id) is None


@pytest.mark.asyncio
async def test_create_can_be_rolled_back(note_block_repo, db_session, block):
    await note_block_repo.create(block)
    block_id = block.id
    db_session.rollback()
    assert await note_block_repo.get(block_id) is None


@pytest.fixture
def ordered_blocks(db_session, course_note):
    blocks = [
        NoteBlock(
            course_note_id=course_note.id,
            title=f"Block {position}",
            content={},
            position=position,
        )
        for position in range(3)
    ]
    db_session.add_all(blocks)
    db_session.commit()
    return blocks


@pytest.mark.asyncio
async def test_reorder_persists_requested_order(
    note_block_repo, db_session, course_note, ordered_blocks
):
    requested = [block.id for block in reversed(ordered_blocks)]
    note_block_repo.reorder(course_note.id, requested)
    db_session.expunge_all()
    found = await note_block_repo.list_by_note(course_note.id)
    assert [block.id for block in found] == requested
    assert [block.position for block in found] == [0, 1, 2]


@pytest.mark.parametrize("invalid_order", ["duplicate", "omitted", "foreign"])
@pytest.mark.asyncio
async def test_reorder_rejects_invalid_ids_without_changing_positions(
    note_block_repo, db_session, course_note, ordered_blocks, invalid_order
):
    original = [block.id for block in ordered_blocks]
    requested = original.copy()
    if invalid_order == "duplicate":
        requested[1] = requested[0]
    elif invalid_order == "omitted":
        requested.pop()
    else:
        other_note = CourseNote(
            course_id=course_note.course_id,
            file_id=course_note.file_id,
            title="Other note",
            resource_type=CourseContentType.LECTURE,
        )
        # A different course/file pair is required by the unique constraint.
        other_file = File(
            owner_id=course_note.file.owner_id,
            original_name="other.pdf",
            storage_key=f"tests/{uuid4().hex}/other.pdf",
        )
        db_session.add(other_file)
        db_session.flush()
        other_note.file_id = other_file.id
        db_session.add(other_note)
        db_session.flush()
        other_block = NoteBlock(
            course_note_id=other_note.id,
            title="Other block",
            content={},
            position=0,
        )
        db_session.add(other_block)
        db_session.commit()
        requested[-1] = other_block.id

    with pytest.raises(ValueError):
        note_block_repo.reorder(course_note.id, requested)

    db_session.expunge_all()
    found = await note_block_repo.list_by_note(course_note.id)
    assert [block.id for block in found] == original
    assert [block.position for block in found] == [0, 1, 2]


@pytest.mark.asyncio
async def test_deleting_course_note_deletes_its_blocks(
    note_block_repo, db_session, course_note, ordered_blocks
):
    note_id = course_note.id
    block_ids = [block.id for block in ordered_blocks]

    db_session.delete(course_note)
    db_session.commit()
    db_session.expunge_all()

    assert db_session.get(CourseNote, note_id) is None
    for block_id in block_ids:
        assert await note_block_repo.get(block_id) is None


@pytest.mark.asyncio
async def test_reorder_can_be_rolled_back(
    note_block_repo, db_session, course_note, ordered_blocks
):
    original = [block.id for block in ordered_blocks]
    note_block_repo.reorder(course_note.id, original[::-1])
    db_session.rollback()
    found = await note_block_repo.list_by_note(course_note.id)
    assert [block.id for block in found] == original
    assert [block.position for block in found] == [0, 1, 2]

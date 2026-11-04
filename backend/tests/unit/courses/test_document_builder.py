from uuid import uuid4

import pytest
from langchain_core.documents import Document
from pydantic import ValidationError

from backend.courses.models import (
    Course,
    CourseContentType,
    CourseNote,
    NoteBlock,
)
from backend.courses.service.document_builder import (
    NoteBlockDocumentBuilder,
    NoteBlockMetadata,
)
from backend.storage.models import File


@pytest.fixture
def builder():
    return NoteBlockDocumentBuilder()


@pytest.fixture
def block():
    owner_id = uuid4()
    course = Course(name="Mechanics", owner_id=owner_id)
    file = File(
        owner_id=owner_id,
        original_name="lecture.pdf",
        storage_key="courses/mechanics/lecture.pdf",
        content_type="application/pdf",
    )
    note = CourseNote(
        course_id=course.id,
        file_id=file.id,
        title="Lecture",
        resource_type=CourseContentType.LECTURE,
    )
    note.course = course
    note.file = file
    block = NoteBlock(
        course_note_id=note.id,
        title="Newton's laws",
        kind="lecture_summary",
        position=0,
        page_start=0,
        page_end=2,
        revision=3,
        content={
            "title": "Newton's laws",
            "summary": "Force changes momentum.",
            "topics": ["Force", "Momentum"],
            "objectives": ["Explain Newton's laws"],
            "prerequisites": [],
            "kind": "conceptual",
        },
    )
    block.course_note = note
    return block


@pytest.mark.asyncio
async def test_get_metadata_includes_source_references(builder, block):
    metadata = await builder.get_metadata(block)
    assert isinstance(metadata, NoteBlockMetadata)
    assert metadata.note_block_id == block.id
    assert metadata.course_note_id == block.course_note_id
    assert metadata.course_id == block.course_note.course_id
    assert metadata.source_file_id == block.course_note.file_id
    assert metadata.filename == "lecture.pdf"
    assert metadata.course_name == "Mechanics"
    assert metadata.revision == 3


@pytest.mark.asyncio
async def test_to_document_renders_content_and_serializes_metadata(builder, block):
    document = await builder.to_document(block)
    assert isinstance(document, Document)
    assert document.id == str(block.id)
    assert "Force changes momentum." in document.page_content
    assert "### Topics" in document.page_content
    assert document.metadata["note_block_id"] == str(block.id)
    assert document.metadata["course_note_id"] == str(block.course_note_id)
    assert document.metadata["course_id"] == str(block.course_note.course_id)
    assert document.metadata["source_file_id"] == str(block.course_note.file_id)
    assert document.metadata["page_start"] == 0
    assert document.metadata["page_end"] == 2
    assert "download_url" not in document.metadata
    assert "course_note" not in document.metadata
    assert "couse_note_id" not in document.metadata


@pytest.mark.asyncio
async def test_to_document_omits_unknown_optional_metadata(builder, block):
    block.page_start = None
    block.page_end = None
    block.course_note.file.content_type = None
    document = await builder.to_document(block)
    assert "page_start" not in document.metadata
    assert "page_end" not in document.metadata
    assert "content_type" not in document.metadata


@pytest.mark.asyncio
async def test_missing_course_note_is_rejected(builder, block):
    block.course_note = None
    with pytest.raises(ValueError, match="no source course note"):
        await builder.to_document(block)


@pytest.mark.parametrize(
    ("attribute", "value", "message"),
    [
        ("schema_version", 2, "Unsupported schema version"),
        ("kind", None, "has no kind"),
        ("kind", "unknown", "Unsupported block kind"),
    ],
)
@pytest.mark.asyncio
async def test_unsupported_content_is_rejected(
    builder, block, attribute, value, message
):
    setattr(block, attribute, value)
    with pytest.raises(ValueError, match=message):
        await builder.to_document(block)


@pytest.mark.asyncio
async def test_invalid_content_is_rejected(builder, block):
    block.content = {"title": "Missing required fields"}
    with pytest.raises(ValidationError):
        await builder.to_document(block)


@pytest.mark.asyncio
async def test_build_preserves_input_order(builder, block):
    other = block.model_copy(update={"id": uuid4()})
    documents = await builder.build([other, block])
    assert [document.id for document in documents] == [str(other.id), str(block.id)]


@pytest.mark.asyncio
async def test_build_empty_input_returns_empty_list(builder):
    assert await builder.build([]) == []

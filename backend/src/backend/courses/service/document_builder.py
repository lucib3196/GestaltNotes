import json
from uuid import UUID

from langchain_core.documents import Document
from pydantic import BaseModel, Field

from backend.courses.models import NOTE_BLOCK_CONTENT_MODELS, NoteBlock
from backend.indexer.indexer import DocumentBuilder


class NoteBlockMetadata(BaseModel):
    """Source references and block state stored with an embedding."""

    note_block_id: UUID = Field(
        description="ID of the editable block that produced this document."
    )
    course_note_id: UUID = Field(
        description="ID of the course resource containing this block."
    )
    course_id: UUID = Field(description="ID of the course that owns the resource.")
    source_file_id: UUID = Field(
        description="ID of the uploaded file associated with the course resource."
    )
    title: str = Field(description="Display title of the block.")
    kind: str = Field(
        description=(
            "Structured content category, such as lecture_summary, "
            "conceptual_question, derivation, or extracted_question."
        )
    )
    position: int = Field(
        ge=0, description="Zero-based display position within the course note."
    )
    revision: int = Field(
        ge=0, description="Block revision used to generate this document."
    )
    schema_version: int = Field(
        ge=1, description="Version of the block's structured content schema."
    )
    page_start: int | None = Field(
        default=None,
        ge=0,
        description="Zero-based first source page, inclusive, when known.",
    )
    page_end: int | None = Field(
        default=None,
        ge=0,
        description="Zero-based last source page, inclusive, when known.",
    )
    filename: str = Field(description="Original name of the uploaded source file.")
    storage_key: str = Field(
        description="Object-storage key identifying the source file's blob."
    )
    content_type: str | None = Field(
        default=None, description="MIME type of the source file, when known."
    )
    course_name: str = Field(
        description="Course display name at the time this document was built."
    )


class NoteBlockDocumentBuilder(DocumentBuilder[NoteBlock]):
    async def get_metadata(self, block: NoteBlock) -> NoteBlockMetadata:
        note = block.course_note
        if note is None:
            raise ValueError(f"Block '{block.id}' has no source course note")

        file = note.file
        course = note.course
        if file is None or course is None:
            raise ValueError(f"Course note '{note.id}' is missing its file or course")
        if not block.kind:
            raise ValueError(f"Block '{block.id}' has no kind")

        return NoteBlockMetadata(
            note_block_id=block.id,
            course_note_id=note.id,
            course_id=note.course_id,
            source_file_id=note.file_id,
            title=block.title,
            kind=block.kind,
            position=block.position,
            revision=block.revision,
            schema_version=block.schema_version,
            page_start=block.page_start,
            page_end=block.page_end,
            filename=file.original_name,
            storage_key=file.storage_key,
            content_type=file.content_type,
            course_name=course.name,
        )

    async def to_document(self, data: NoteBlock) -> Document:
        text = self.get_page_content(data)
        if not text.strip():
            raise ValueError(f"Block '{data.id}' produced empty text")
        metadata = await self.get_metadata(data)
        return Document(
            id=str(data.id),
            page_content=text,
            metadata=metadata.model_dump(mode="json", exclude_none=True),
        )

    @staticmethod
    def get_page_content(block: NoteBlock) -> str:
        if block.schema_version != 1:
            raise ValueError(f"Unsupported schema version: {block.schema_version}")
        if not block.kind:
            raise ValueError(f"Block '{block.id}' has no kind")
        model = NOTE_BLOCK_CONTENT_MODELS.get(block.kind)
        if model is None:
            raise ValueError(f"Unsupported block kind: {block.kind}")

        content = model.model_validate(block.content)
        render = getattr(content, "as_string", None)
        if callable(render):
            text = render()
            if not isinstance(text, str):
                raise TypeError("as_string() must return a string")
            return text
        return json.dumps(content.model_dump(mode="json"), ensure_ascii=False)

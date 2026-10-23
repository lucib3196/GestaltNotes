from pydantic import BaseModel, Field


class NoteBlockDocumentMetadata(BaseModel):
    """Metadata attached to an indexed note-block document."""

    note_block_id: str = Field(description="UUID of the source note block.")
    title: str
    kind: str
    position: int
    revision: int
    schema_version: int = Field(
        description="Version of the note block's content schema.",
    )

    course_id: str | None = None
    course_name: str | None = None

    source_file_id: str | None = None
    filename: str | None = None
    storage_key: str | None = None
    content_type: str | None = None
    download_url: str | None = None

    page_start: int | None = None
    page_end: int | None = None

import asyncio
import json
from typing import Self
from uuid import UUID

from langchain_core.documents import Document
from object_store import BlobStorage
from sqlmodel import Session

from backend.storage import FileService

from .models import NOTE_BLOCK_CONTENT_MODELS, NoteBlock


class NoteBlockDocumentBuilder:
    def __init__(self, files: FileService) -> None:
        self._files = files

    @classmethod
    def from_dependencies(
        cls,
        *,
        session: Session,
        storage: BlobStorage,
    ) -> Self:
        files = FileService(
            session=session,
            storage=storage,
        )
        return cls(files=files)

    async def build(
        self, blocks: list[NoteBlock], *, include_url: bool = True
    ) -> list[Document]:
        documents = await asyncio.gather(
            *[self.note_block_to_document(b) for b in blocks]
        )
        # Set of file ids. Reused for blocks sharing the same source
        # Focused on file metadata
        file_ids = {
            block.source_file_id for block in blocks if block.source_file_id is not None
        }
        metadata_by_file: dict[UUID, dict[str, str]] = {}
        for file_id in file_ids:
            file = await self._files.get_file(file_id)
            metadata = {
                "filename": file.original_name,
                "storage_key": file.storage_key,
            }
            if file.content_type is not None:
                metadata["content_type"] = file.content_type
            if include_url:
                metadata["download_url"] = await self._files.get_download_url(file_id)
            metadata_by_file[file_id] = metadata

        for block, document in zip(blocks, documents, strict=False):
            if block.source_file_id is not None:
                document.metadata.update(metadata_by_file[block.source_file_id])
            if block.course:
                document.metadata.update(
                    course_name=block.course.name, course_id=str(block.course.id)
                )
        return documents

    @staticmethod
    async def note_block_to_document(block: NoteBlock) -> Document:
        if block.schema_version != 1:
            raise ValueError(f"Unsupported schema version: {block.schema_version}")
        if not block.kind:
            raise ValueError(f"Cannot determine kind for block. {block.id}")
        model = NOTE_BLOCK_CONTENT_MODELS.get(block.kind)
        if model is None:
            raise ValueError(f"Cannot Determine Model for block of kind {block.kind}")

        content = model.model_validate(block.content)
        metadata = {
            "note_block_id": str(block.id),
            "title": block.title,
            "kind": block.kind,
            "position": block.position,
            "revision": block.revision,
            "schema_version": block.schema_version,
        }
        if block.course_id is not None:
            metadata["course_id"] = str(block.course_id)
        if block.source_file_id is not None:
            metadata["source_file_id"] = str(block.source_file_id)
        if block.page_start is not None:
            metadata["page_start"] = block.page_start
        if block.page_end is not None:
            metadata["page_end"] = block.page_end

        render = getattr(content, "as_string", None)
        if callable(render):
            text = render()
            if not isinstance(text, str):
                raise TypeError("as_string() must return a string")
        else:
            text = json.dumps(content.model_dump(mode="json"))
        return Document(id=str(block.id), page_content=text, metadata=metadata)

from typing import Any
from uuid import UUID

from lecture_processor.extract_derivations.model import Derivation
from lecture_processor.extracted_question import ExtractedQuestion
from lecture_processor.graph.state import OutputState
from pydantic import BaseModel
from langchain_core.documents import Document
from .models import NoteBlock

from .models import NOTE_BLOCK_CONTENT_MODELS


def parse_lecture_document(
    source: Any | OutputState,
    *,
    source_file_id: UUID | None = None,
    course_id: UUID | None = None,
) -> list[NoteBlock]:
    data = OutputState.model_validate(source)
    notes: list[NoteBlock] = []

    def append_block(
        item: BaseModel,
        *,
        title: str,
        kind: str,
        page_start: int | None = None,
        page_end: int | None = None,
    ) -> None:
        notes.append(
            NoteBlock(
                source_file_id=source_file_id,
                course_id=course_id,
                title=title,
                kind=kind,
                content=item.model_dump(mode="json"),
                position=len(notes),
                page_start=page_start,
                page_end=page_end,
            )
        )

    if data.lecture_summary is not None:
        summary = data.lecture_summary
        append_block(summary, title=summary.title, kind="lecture_summary")

    for question in data.conceptual_questions:
        reference = question.reference
        append_block(
            question,
            title=question.question,
            kind="conceptual_question",
            page_start=reference.start if reference is not None else None,
            page_end=reference.end if reference is not None else None,
        )

    for section in sorted(data.results, key=lambda section: section.index):
        for item in section.items:
            if isinstance(item, Derivation):
                title = item.title
                kind = "derivation"
            elif isinstance(item, ExtractedQuestion):
                title = item.question
                kind = "extracted_question"
            else:
                raise TypeError(f"Unsupported item type: {type(item).__name__}")

            reference = item.reference
            append_block(
                item,
                title=title,
                kind=kind,
                page_start=reference.start if reference is not None else None,
                page_end=reference.end if reference is not None else None,
            )

    return notes


def note_blocks_to_documents(blocks: list[NoteBlock]) -> list[Document]:
    documents = []

    for block in blocks:
        if block.schema_version != 1:
            raise ValueError(f"Unsupported schema version: {block.schema_version}")

        model = NOTE_BLOCK_CONTENT_MODELS.get(block.kind)
        if model is None:
            raise ValueError(f"Unsupported block kind: {block.kind}")

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

        documents.append(
            Document(
                id=str(block.id),
                page_content=content.as_string(),
                metadata=metadata,
            )
        )

    return documents


if __name__ == "__main__":
    from pathlib import Path
    import json
    import backend.accounts.models
    import backend.storage.models

    path = Path(
        r"/home/lberm/projects/gestalt/GestaltNotes/packages/lecture_processor/src/full_output.json"
    )
    content = json.loads(path.read_text())
    notes = parse_lecture_document(content)
    print(len(notes))
    docs = note_blocks_to_documents(notes)
    print(docs[-1])

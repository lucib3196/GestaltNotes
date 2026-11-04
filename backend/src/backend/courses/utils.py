from typing import Any
from uuid import UUID

from lecture_processor.conceptual_question import ConceptualQuestion
from lecture_processor.extract_derivations.model import Derivation
from lecture_processor.extracted_question import ExtractedQuestion
from lecture_processor.graph.state import OutputState
from lecture_processor.lecture_analysis import LectureAnalysis
from pydantic import ValidationError

from backend.courses.exceptions import (
    NoteBlockValidationError,
)
from backend.courses.models import NOTE_BLOCK_CONTENT_MODELS, NoteBlock


def validate_note_block(
    block: NoteBlock,
    content: dict[str, Any] | None = None,
) -> dict[str, Any]:
    if block.schema_version != 1:
        raise NoteBlockValidationError(
            f"Unsupported schema version: {block.schema_version}"
        )

    if not block.kind:
        raise NoteBlockValidationError("Block kind is required")

    model = NOTE_BLOCK_CONTENT_MODELS.get(block.kind)
    if model is None:
        raise NoteBlockValidationError(f"Unsupported block kind: {block.kind}")

    payload = block.content if content is None else content

    try:
        return model.model_validate(payload).model_dump(mode="json")
    except ValidationError as exc:
        raise NoteBlockValidationError(
            f"Invalid content for block kind '{block.kind}': {exc}"
        ) from exc


ExtractedItem = LectureAnalysis | ConceptualQuestion | Derivation | ExtractedQuestion

BLOCK_KIND_BY_MODEL = {model: kind for kind, model in NOTE_BLOCK_CONTENT_MODELS.items()}


def parse_lecture_document(
    source: object,
    *,
    course_note_id: UUID,
) -> list[NoteBlock]:
    data = OutputState.model_validate(source)
    blocks: list[NoteBlock] = []

    def append_block(item: ExtractedItem) -> None:
        kind = BLOCK_KIND_BY_MODEL.get(type(item))
        if kind is None:
            raise TypeError(f"Unsupported item type: {type(item).__name__}")

        reference = None if isinstance(item, LectureAnalysis) else item.reference

        blocks.append(
            NoteBlock(
                course_note_id=course_note_id,
                title=item.title,
                kind=kind,
                content=item.model_dump(mode="json"),
                position=len(blocks),
                page_start=reference.start if reference is not None else None,
                page_end=reference.end if reference is not None else None,
            )
        )

    if data.lecture_summary is not None:
        append_block(data.lecture_summary)

    for question in data.conceptual_questions:
        append_block(question)

    for section in sorted(data.results, key=lambda section: section.index):
        for item in section.items:
            append_block(item)

    return blocks

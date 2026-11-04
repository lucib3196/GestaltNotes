from typing import Any

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

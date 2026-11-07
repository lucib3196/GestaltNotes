from uuid import UUID

from fastapi import APIRouter, HTTPException, Response
from pydantic import ValidationError
from starlette import status

from backend.core.logger import logger
from backend.courses.exceptions import (
    NoteBlockNotFoundError,
    NoteBlockValidationError,
)
from backend.courses.models import NoteBlock, NoteBlockRead, NoteBlockUpdate
from backend.web.courses.dependencies import (
    NoteBlockServiceDep,
    OwnedNoteBlockDep,
    ReadableNoteBlockDep,
    ReadableNoteBlockRepoDep,
)

router = APIRouter(
    prefix="/courses/{course_id}/blocks",
    tags=["courses", "note blocks"],
)


def block_http_exception(exc: Exception, *, operation: str) -> HTTPException:
    """Keep block validation errors distinct from persistence/provider failures."""
    if isinstance(exc, HTTPException):
        return exc
    if isinstance(exc, NoteBlockNotFoundError):
        return HTTPException(status.HTTP_404_NOT_FOUND, "Note block not found")
    if isinstance(exc, (NoteBlockValidationError, ValidationError)):
        return HTTPException(status.HTTP_422_UNPROCESSABLE_ENTITY, str(exc))
    logger.exception("Block operation failed: operation=%s", operation)
    detail = f"Could not {operation} this note block."
    if operation == "update":
        detail += (
            " The edit may have been saved before indexing failed."
            " Reload before retrying."
        )
    return HTTPException(status.HTTP_500_INTERNAL_SERVER_ERROR, detail)


@router.get("", response_model=list[NoteBlockRead])
async def list_note_blocks(
    course_id: UUID,
    blocks: ReadableNoteBlockRepoDep,
    source_file_id: UUID | None = None,
    course_note_id: UUID | None = None,
) -> list[NoteBlock]:
    """Read blocks with database filters; no vector-store configuration is needed."""
    return list(
        await blocks.list_by_course(
            course_id,
            course_note_id=course_note_id,
            source_file_id=source_file_id,
        )
    )


@router.get("/{block_id}", response_model=NoteBlockRead)
async def get_note_block(block: ReadableNoteBlockDep) -> NoteBlock:
    return block


@router.patch("/{block_id}", response_model=NoteBlockRead)
async def update_note_block(
    update: NoteBlockUpdate,
    block: OwnedNoteBlockDep,
    service: NoteBlockServiceDep,
) -> NoteBlock:
    """Save and reindex an owned block; currently uses last-write-wins edits."""
    try:
        return await service.update(block.id, update)
    except Exception as exc:
        raise block_http_exception(exc, operation="update") from exc


@router.delete("/{block_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_note_block(
    block: OwnedNoteBlockDep,
    service: NoteBlockServiceDep,
) -> Response:
    """Remove both the block's indexed document and database record."""
    try:
        await service.delete(block.id)
    except Exception as exc:
        raise block_http_exception(exc, operation="delete") from exc
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.post("/{block_id}/reindex", status_code=status.HTTP_204_NO_CONTENT)
async def reindex_note_block(
    block: OwnedNoteBlockDep,
    service: NoteBlockServiceDep,
    force_recreate: bool = False,
) -> Response:
    """Index current content synchronously without repeating document extraction."""
    try:
        await service.reindex(block.id, force_recreate=force_recreate)
    except Exception as exc:
        raise block_http_exception(exc, operation="reindex") from exc
    return Response(status_code=status.HTTP_204_NO_CONTENT)

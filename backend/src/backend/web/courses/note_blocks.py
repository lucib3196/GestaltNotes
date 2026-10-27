from uuid import UUID

from fastapi import APIRouter, HTTPException

from backend.courses.notes.models import NoteBlock
from backend.courses.notes.schema import NoteBlockRead
from backend.web.courses.dependencies import NoteBlockServiceDep, ReadableCourseDep

router = APIRouter(
    prefix="/courses/{course_id}/blocks",
    tags=["courses", "note blocks"],
)


@router.get("", response_model=list[NoteBlockRead])
async def list_note_blocks(
    course_id: UUID,
    service: NoteBlockServiceDep,
    _course: ReadableCourseDep,
    source_file_id: UUID | None = None,
) -> list[NoteBlock]:
    blocks = service.list_by_course(course_id)
    if source_file_id is not None:
        blocks = [block for block in blocks if block.source_file_id == source_file_id]
    return blocks


@router.get("/{block_id}", response_model=NoteBlockRead)
async def get_note_block(
    course_id: UUID,
    block_id: UUID,
    service: NoteBlockServiceDep,
    _course: ReadableCourseDep,
) -> NoteBlock:
    block = service.get(block_id)
    if block is None or block.course_id != course_id:
        raise HTTPException(status_code=404, detail="Note block not found")
    return block

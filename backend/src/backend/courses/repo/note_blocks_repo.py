from collections.abc import Sequence
from datetime import datetime
from uuid import UUID

from sqlmodel import Session, col, select

from backend.adapters import Repository
from backend.courses.models import CourseNote, NoteBlock, NoteBlockUpdate


class NoteBlockRepo(Repository[NoteBlock, NoteBlockUpdate]):
    def __init__(self, session: Session) -> None:
        self._session = session

    async def create(self, record: NoteBlock) -> NoteBlock:
        self._session.add(record)
        self._session.flush()
        self._session.refresh(record)
        return record

    async def get(self, record_id: UUID) -> NoteBlock | None:
        return self._session.exec(
            select(NoteBlock).where(NoteBlock.id == record_id)
        ).first()

    async def update(self, record: NoteBlock, update: NoteBlockUpdate) -> NoteBlock:
        for key, value in update.model_dump(exclude_unset=True).items():
            setattr(record, key, value)
        self._session.add(record)
        self._session.flush()
        self._session.refresh(record)
        return record

    async def update_by_id(self, record_id: UUID, update: NoteBlockUpdate) -> NoteBlock:
        note = await self.get(record_id)
        if note is None:
            raise ValueError()
        return await self.update(note, update)

    async def delete(self, record_id: UUID) -> None:
        note = await self.get(record_id)
        if note is not None:
            self._session.delete(note)
            self._session.flush()

    # Listing
    async def list_by_note(self, note_id: UUID) -> Sequence[NoteBlock]:
        statement = (
            select(NoteBlock)
            .join(CourseNote, col(NoteBlock.course_note_id) == CourseNote.id)
            .where(CourseNote.id == note_id)
            .order_by(col(NoteBlock.position), col(NoteBlock.id))
        )
        return self._session.exec(statement).all()

    async def list_by_course(self, course_id: UUID) -> Sequence[NoteBlock]:
        statement = (
            select(NoteBlock)
            .join(CourseNote, col(NoteBlock.course_note_id) == CourseNote.id)
            .where(CourseNote.course_id == course_id)
            .order_by(col(NoteBlock.position), col(NoteBlock.id))
        )
        return self._session.exec(statement).all()

    async def list_by_file(self, file_id: UUID) -> Sequence[NoteBlock]:
        statement = (
            select(NoteBlock)
            .join(CourseNote, col(NoteBlock.course_note_id) == CourseNote.id)
            .where(CourseNote.file_id == file_id)
            .order_by(col(NoteBlock.position), col(NoteBlock.id))
        )
        return self._session.exec(statement).all()

    # Attribute access
    async def get_note(self, block_id: UUID) -> CourseNote | None:
        block = await self.get(block_id)
        if block is not None:
            return block.course_note
        return None

    # Special Updates
    def reorder(self, course_note_id: UUID, block_ids: list[UUID]) -> None:
        if len(block_ids) != len(set(block_ids)):
            raise ValueError("Block IDs must not contain duplicates")

        statement = (
            select(NoteBlock)
            .where(NoteBlock.course_note_id == course_note_id)
            .with_for_update()
        )

        blocks = list(self._session.exec(statement).all())
        by_id = {block.id: block for block in blocks}

        if set(block_ids) != set(by_id):
            raise ValueError(
                "Provide every block belonging to the course note exactly once"
            )

        now = datetime.utcnow()
        for position, block_id in enumerate(block_ids):
            block = by_id[block_id]
            block.position = position
            block.updated_at = now
            self._session.add(block)

        self._session.flush()

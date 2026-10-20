from uuid import UUID

from sqlmodel import Session, select

from backend.courses.notes.models import NoteBlock


class NoteBlockService:
    def __init__(self, session: Session) -> None:
        self._session = session

    def add(self, block: NoteBlock) -> NoteBlock:
        try:
            self._session.add(block)
            self._session.commit()
            self._session.refresh(block)
            return block
        except Exception:
            self._session.rollback()
            raise

    def get(self, block_id: UUID) -> NoteBlock | None:
        return self._session.get(NoteBlock, block_id)

    def list_by_file(self, file_id: UUID) -> list[NoteBlock]:
        statement = select(NoteBlock).where(
            NoteBlock.source_file_id == file_id
        )
        return list(self._session.exec(statement).all())

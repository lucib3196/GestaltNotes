from datetime import datetime
from typing import Any
from uuid import UUID

from sqlalchemy import update
from sqlmodel import Session, select

from backend.courses.notes.models import NOTE_BLOCK_CONTENT_MODELS, NoteBlock


class NoteBlockNotFoundError(LookupError):
    pass


class NoteBlockRevisionConflictError(ValueError):
    pass


class NoteBlockService:
    def __init__(self, session: Session) -> None:
        self._session = session

    def create(self, block: NoteBlock) -> NoteBlock:
        return self.create_many([block])[0]

    def add(self, block: NoteBlock) -> NoteBlock:
        """Compatibility with existing callers."""
        return self.create(block)

    def create_many(self, blocks: list[NoteBlock]) -> list[NoteBlock]:
        # SQLModel table construction alone is not the validation boundary.
        validated = []
        for block in blocks:
            candidate = NoteBlock.model_validate(block.model_dump())
            candidate.content = self._validate_content(candidate)
            self._validate_pages(candidate)
            validated.append(candidate)

        try:
            self._session.add_all(validated)
            self._session.commit()
        except Exception:
            self._session.rollback()
            raise

        for block in validated:
            self._session.refresh(block)
        return validated

    def get(self, block_id: UUID) -> NoteBlock | None:
        return self._session.get(NoteBlock, block_id)

    def get_or_raise(self, block_id: UUID) -> NoteBlock:
        block = self.get(block_id)
        if block is None:
            raise NoteBlockNotFoundError(f"Note block '{block_id}' not found")
        return block

    def list_by_file(self, file_id: UUID) -> list[NoteBlock]:
        statement = (
            select(NoteBlock)
            .where(NoteBlock.source_file_id == file_id)
            .order_by(NoteBlock.position, NoteBlock.id)
        )
        return list(self._session.exec(statement).all())

    def list_by_course(self, course_id: UUID) -> list[NoteBlock]:
        statement = (
            select(NoteBlock)
            .where(NoteBlock.course_id == course_id)
            .order_by(NoteBlock.position, NoteBlock.id)
        )
        return list(self._session.exec(statement).all())

    def update_content(
        self,
        block_id: UUID,
        *,
        content: dict[str, Any],
        expected_revision: int,
    ) -> NoteBlock:
        block = self.get_or_raise(block_id)
        validated_content = self._validate_content(block, content)
        return self._update_revision(
            block_id, expected_revision, {"content": validated_content}
        )

    def update_title(
        self,
        block_id: UUID,
        *,
        title: str,
        expected_revision: int,
    ) -> NoteBlock:
        title = title.strip()
        if not title:
            raise ValueError("Title must not be empty")
        return self._update_revision(block_id, expected_revision, {"title": title})

    def reorder(self, file_id: UUID, block_ids: list[UUID]) -> None:
        if len(block_ids) != len(set(block_ids)):
            raise ValueError("Block IDs must not contain duplicates")

        try:
            statement = (
                select(NoteBlock)
                .where(NoteBlock.source_file_id == file_id)
                .with_for_update()
            )
            blocks = self._session.exec(statement).all()
            by_id = {block.id: block for block in blocks}
            if set(block_ids) != set(by_id):
                raise ValueError(
                    "Provide every block belonging to the file exactly once"
                )

            now = datetime.utcnow()
            for position, block_id in enumerate(block_ids):
                block = by_id[block_id]
                block.position = position
                block.updated_at = now
                self._session.add(block)
            self._session.commit()
        except Exception:
            self._session.rollback()
            raise

    def delete(self, block_id: UUID) -> None:
        try:
            block = self.get_or_raise(block_id)
            self._session.delete(block)
            self._session.commit()
        except Exception:
            self._session.rollback()
            raise

    def _validate_content(
        self,
        block: NoteBlock,
        content: dict[str, Any] | None = None,
    ) -> dict[str, Any]:
        if block.schema_version != 1:
            raise ValueError(f"Unsupported schema version: {block.schema_version}")
        model = NOTE_BLOCK_CONTENT_MODELS.get(block.kind)
        if model is None:
            raise ValueError(f"Unsupported block kind: {block.kind}")
        payload = block.content if content is None else content
        return model.model_validate(payload).model_dump(mode="json")

    @staticmethod
    def _validate_pages(block: NoteBlock) -> None:
        if (
            block.page_start is not None
            and block.page_end is not None
            and block.page_end < block.page_start
        ):
            raise ValueError("page_end must be >= page_start")

    def _update_revision(
        self,
        block_id: UUID,
        expected_revision: int,
        values: dict[str, Any],
    ) -> NoteBlock:
        if expected_revision < 0:
            raise ValueError("Expected revision must be nonnegative")
        try:
            statement = (
                update(NoteBlock)
                .where(
                    NoteBlock.id == block_id,
                    NoteBlock.revision == expected_revision,
                )
                .values(
                    **values,
                    revision=NoteBlock.revision + 1,
                    updated_at=datetime.utcnow(),
                )
                .returning(NoteBlock)
            )
            block = self._session.execute(
                statement,
                execution_options={"populate_existing": True},
            ).scalar_one_or_none()
            if block is None:
                self.get_or_raise(block_id)
                raise NoteBlockRevisionConflictError(
                    "The block changed; reload it before saving"
                )
            self._session.commit()
        except Exception:
            self._session.rollback()
            raise
        self._session.refresh(block)
        return block

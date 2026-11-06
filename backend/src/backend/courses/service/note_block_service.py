from datetime import UTC, datetime
from typing import Any
from uuid import UUID

from pydantic import ValidationError
from sqlalchemy.exc import SQLAlchemyError
from sqlmodel import Session

from backend.core.logger import logger
from backend.courses.exceptions import (
    NoteBlockCreationError,
    NoteBlockDeletionError,
    NoteBlockNotFoundError,
    NoteBlockRetrievalError,
    NoteBlockUpdateError,
    NoteBlockValidationError,
)
from backend.courses.models import NOTE_BLOCK_CONTENT_MODELS, NoteBlock, NoteBlockUpdate
from backend.courses.repo.note_blocks_repo import NoteBlockRepo
from backend.indexer.indexer import IndexingService


class NoteBlockService:
    def __init__(
        self,
        session: Session,
        blocks: NoteBlockRepo,
        indexer: IndexingService[NoteBlock, NoteBlockUpdate],
    ) -> None:
        self._session = session
        self._blocks = blocks
        self._indexer = indexer

    async def create(self, block: NoteBlock) -> NoteBlock:
        """Validate, save, and index one block.

        Indexing runs after commit; indexing failure does not undo the saved block.
        """
        return (await self.create_many([block]))[0]

    async def create_many(self, blocks: list[NoteBlock]) -> list[NoteBlock]:
        """Validate and save all blocks in one transaction, then index them.

        Indexing stops at the first failure; saved blocks remain committed.
        """
        if not blocks:
            return []

        try:
            validated = []
            for block in blocks:
                candidate = NoteBlock.model_validate(block.model_dump())
                candidate.content = self.validate_note_block(candidate)
                validated.append(candidate)

            saved = []
            for block in validated:
                saved.append(await self._blocks.create(block))

            self._session.commit()
        except SQLAlchemyError as exc:
            self._session.rollback()
            logger.exception("Note block creation failed: count=%d", len(blocks))
            raise NoteBlockCreationError("Could not create note blocks") from exc
        except Exception:
            self._session.rollback()
            raise

        logger.info("Note blocks saved: count=%d", len(saved))
        await self._indexer.index_many([block.id for block in saved])
        return saved

    async def get(self, block_id: UUID) -> NoteBlock:
        """Return a block by ID, raising NoteBlockNotFoundError if absent."""
        try:
            block = await self._blocks.get(block_id)
        except SQLAlchemyError as exc:
            logger.exception("Note block retrieval failed: block_id=%s", block_id)
            raise NoteBlockRetrievalError(
                f"Could not retrieve note block '{block_id}'"
            ) from exc

        if block is None:
            raise NoteBlockNotFoundError(f"Note block '{block_id}' not found")

        return block

    async def update(
        self,
        block_id: UUID,
        update: NoteBlockUpdate,
    ) -> NoteBlock:
        """Validate changes, increment the revision, commit, then reindex the block.

        Indexing failure does not undo the committed edit.
        """
        try:
            block = await self.get(block_id)
            changes = update.model_dump(exclude_unset=True)

            if not changes:
                raise NoteBlockValidationError("Provide at least one field to update")

            if "content" in changes:
                changes["content"] = self.validate_note_block(block, changes["content"])

            validated_update = NoteBlockUpdate.model_validate(changes)

            block.revision += 1
            block.updated_at = datetime.now(UTC).replace(tzinfo=None)

            saved = await self._blocks.update(block, validated_update)
            self._session.commit()
        except SQLAlchemyError as exc:
            self._session.rollback()
            logger.exception("Note block update failed: block_id=%s", block_id)
            raise NoteBlockUpdateError(
                f"Could not update note block '{block_id}'"
            ) from exc
        except Exception:
            self._session.rollback()
            raise

        logger.info(
            "Note block saved: block_id=%s revision=%d fields=%s",
            block_id,
            saved.revision,
            ",".join(sorted(changes)),
        )
        await self._indexer.index(block_id)
        return saved

    async def delete(self, block_id: UUID) -> None:
        """Remove the block's vector, then delete and commit its database row.

        A database failure does not restore an already removed vector.
        """
        try:
            await self.get(block_id)
            await self._indexer.delete([block_id])
            await self._blocks.delete(block_id)
            self._session.commit()
        except SQLAlchemyError as exc:
            self._session.rollback()
            logger.exception("Note block deletion failed: block_id=%s", block_id)
            raise NoteBlockDeletionError(
                f"Could not delete note block '{block_id}'"
            ) from exc
        except Exception:
            self._session.rollback()
            raise

        logger.info("Note block deleted: block_id=%s", block_id)

    async def delete_by_note_id(self, note_id: UUID, *, commit: bool = True) -> None:
        """Remove a note's vectors before deleting its block rows.

        Set commit=False when an outer workflow owns the transaction.
        Cleanup failures propagate; database rollback cannot restore vectors.
        """
        try:
            blocks = await self._blocks.list_by_note(note_id)
            if not blocks:
                return
            await self._indexer.delete([block.id for block in blocks])
            for block in blocks:
                await self._blocks.delete(block.id)
            if commit:
                self._session.commit()
        except Exception:
            logger.exception("Note block cleanup failed: note_id=%s", note_id)
            if commit:
                self._session.rollback()
            raise

    async def reindex(self, block_id: UUID, *, force_recreate: bool = False) -> None:
        """Synchronize an existing block's document without changing its source data.

        Skip unchanged documents unless force_recreate is True.
        """
        await self.get(block_id)
        await self._indexer.index(block_id, force_recreate=force_recreate)

    @staticmethod
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

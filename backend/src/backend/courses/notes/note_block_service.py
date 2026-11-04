from datetime import UTC, datetime
from typing import Self
from uuid import UUID

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
from backend.courses.models import NoteBlock, NoteBlockUpdate
from backend.courses.repo import NoteBlockRepo
from backend.courses.service.document_builder import NoteBlockDocumentBuilder
from backend.courses.utils import validate_note_block
from backend.courses.vector_store.course_vector_store_service import (
    CourseVectorStoreService,
)
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

    @classmethod
    def from_dependencies(cls, session: Session, course_id: UUID) -> Self:
        blocks = NoteBlockRepo(session)
        stores = CourseVectorStoreService(session)
        indexer = IndexingService[NoteBlock, NoteBlockUpdate](
            repo=blocks,
            builder=NoteBlockDocumentBuilder(),
            vector_store=stores.get_vectorstore(course_id, async_mode=True),
        )
        return cls(session, blocks, indexer)

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
                candidate.content = validate_note_block(candidate)
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
                changes["content"] = validate_note_block(block, changes["content"])

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
            await self._indexer.delete(block_id)
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

    async def reindex(self, block_id: UUID, *, force_recreate: bool = False) -> None:
        """Synchronize an existing block's document without changing its source data.

        Skip unchanged documents unless force_recreate is True.
        """
        await self.get(block_id)
        await self._indexer.index(block_id, force_recreate=force_recreate)

    async def list_by_course(self, course_id: UUID) -> list[NoteBlock]:
        """Return blocks belonging to the course without modifying or indexing them."""
        return list(await self._blocks.list_by_course(course_id))

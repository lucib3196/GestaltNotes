from datetime import UTC, datetime
from typing import Any
from uuid import UUID

from pydantic import ValidationError
from sqlalchemy.exc import SQLAlchemyError
from sqlmodel import Session

from backend.courses.exceptions import (
    NoteBlockCreationError,
    NoteBlockDeletionError,
    NoteBlockNotFoundError,
    NoteBlockRetrievalError,
    NoteBlockUpdateError,
    NoteBlockValidationError,
)
from backend.courses.models import NOTE_BLOCK_CONTENT_MODELS, NoteBlock, NoteBlockUpdate
from backend.courses.repo import NoteBlockRepo


class NoteBlockService:
    def __init__(self, session: Session) -> None:
        self._session = session
        self._blocks = NoteBlockRepo(session)

    async def create(self, block: NoteBlock) -> NoteBlock:
        return (await self.create_many([block]))[0]

    async def create_many(self, blocks: list[NoteBlock]) -> list[NoteBlock]:
        if not blocks:
            return []

        try:
            validated = []
            for block in blocks:
                candidate = NoteBlock.model_validate(block.model_dump())
                candidate.content = self._validate_content(candidate)
                validated.append(candidate)

            saved = []
            for block in validated:
                saved.append(await self._blocks.create(block))

            self._session.commit()
            return saved
        except SQLAlchemyError as exc:
            self._session.rollback()
            raise NoteBlockCreationError("Could not create note blocks") from exc
        except Exception:
            self._session.rollback()
            raise

    async def get(self, block_id: UUID) -> NoteBlock:
        try:
            block = await self._blocks.get(block_id)
        except SQLAlchemyError as exc:
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
        try:
            block = await self.get(block_id)
            changes = update.model_dump(exclude_unset=True)

            if not changes:
                raise NoteBlockValidationError("Provide at least one field to update")

            if "content" in changes:
                changes["content"] = self._validate_content(block, changes["content"])

            validated_update = NoteBlockUpdate.model_validate(changes)

            block.revision += 1
            block.updated_at = datetime.now(UTC).replace(tzinfo=None)

            saved = await self._blocks.update(block, validated_update)
            self._session.commit()
            return saved
        except SQLAlchemyError as exc:
            self._session.rollback()
            raise NoteBlockUpdateError(
                f"Could not update note block '{block_id}'"
            ) from exc
        except Exception:
            self._session.rollback()
            raise

    async def delete(self, block_id: UUID) -> None:
        try:
            await self.get(block_id)
            await self._blocks.delete(block_id)
            self._session.commit()
        except SQLAlchemyError as exc:
            self._session.rollback()
            raise NoteBlockDeletionError(
                f"Could not delete note block '{block_id}'"
            ) from exc
        except Exception:
            self._session.rollback()
            raise

    def _validate_content(
        self,
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

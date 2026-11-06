import asyncio
from abc import ABC, abstractmethod
from collections.abc import Sequence
from typing import TypeVar
from uuid import UUID

from langchain_core.documents import Document
from langchain_core.vectorstores import VectorStore
from pydantic import BaseModel

from backend.adapters import Repository
from backend.core.logger import logger

ModelT = TypeVar("ModelT", bound=BaseModel)
UpdateT = TypeVar("UpdateT", bound=BaseModel)


class DocumentBuilder[ModelT: BaseModel](ABC):
    async def build(self, data: Sequence[ModelT]) -> list[Document]:
        """Convert each input into a document."""
        return [await self.to_document(item) for item in data]

    @abstractmethod
    async def to_document(self, data: ModelT) -> Document:
        """Render one input and attach its metadata."""
        ...


class IndexingService[ModelT: BaseModel, UpdateT: BaseModel]:
    def __init__(
        self,
        repo: Repository[ModelT, UpdateT],
        builder: DocumentBuilder[ModelT],
        vector_store: VectorStore,
    ) -> None:
        self._repo = repo
        self._builder = builder
        self._store = vector_store

    async def index(
        self,
        resource_id: UUID,
        *,
        force_recreate: bool = False,
    ) -> list[str]:
        """Load a resource, build its document, and write it to the vector store.

        Skip unchanged text and metadata unless force_recreate is True.
        Does not modify the source database record.
        """
        try:
            block = await self._repo.get(resource_id)
            if block is None:
                raise ValueError(f"Resource '{resource_id}' not found")

            document = await self._builder.to_document(block)
            document_id = document.id
            if not document_id:
                raise ValueError("Expected document to have an ID")

            existing = await self._store.aget_by_ids([document_id])

            if not force_recreate and existing:
                current = existing[0]
                if (
                    current.page_content == document.page_content
                    and current.metadata == document.metadata
                ):
                    logger.debug(
                        "Indexing skipped: resource_id=%s reason=unchanged", resource_id
                    )
                    return []

            logger.info(
                "Document indexed: resource_id=%s document_id=%s forced=%s",
                resource_id,
                document_id,
                force_recreate,
            )
            return await self._store.aadd_documents(
                [document],
                ids=[document_id],
            )
        except Exception:
            logger.exception("Indexing failed: resource_id=%s", resource_id)
            raise

    async def index_many(
        self,
        resource_ids: Sequence[UUID],
        *,
        force_recreate: bool = False,
    ) -> list[str]:
        """Index unique resource IDs sequentially, preserving input order.

        Stop at the first failure; earlier vector writes remain applied.
        """
        results = await asyncio.gather(
            *(
                self.index(resource_id, force_recreate=force_recreate)
                for resource_id in dict.fromkeys(resource_ids)
            )
        )
        return [item for result in results for item in result]

    async def delete(self, ids: list[UUID | str]) -> None:
        """Delete the vector document whose ID matches the resource UUID.

        Does not delete the source database record.
        """
        try:
            result = await self._store.adelete(ids=[str(idx) for idx in ids])
            if result is False:
                raise RuntimeError(f"Could not delete indexed resource '{len(ids)}'")
        except Exception:
            logger.exception("Index deletion failed: resource_id=%s", str(ids))
            raise

        logger.info("Indexed document removed: resource_id=%s", str(ids))

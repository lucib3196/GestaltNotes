from abc import ABC, abstractmethod
from collections.abc import Sequence
from typing import Generic, TypeVar
from uuid import UUID

from langchain_core.documents import Document
from langchain_core.vectorstores import VectorStore
from pydantic import BaseModel

from backend.adapters import Repository

ModelT = TypeVar("ModelT", bound=BaseModel)
UpdateT = TypeVar("UpdateT", bound=BaseModel)


class DocumentBuilder(ABC, Generic[ModelT]):
    async def build(self, data: Sequence[ModelT]) -> list[Document]:
        """Convert each input into a document."""
        return [await self.to_document(item) for item in data]

    @abstractmethod
    async def to_document(self, data: ModelT) -> Document:
        """Render one input and attach its metadata."""
        ...


class IndexingService(Generic[ModelT, UpdateT]):
    def __init__(
        self,
        repo: Repository[ModelT, UpdateT],
        builder: DocumentBuilder[ModelT],
        vector_store: VectorStore,
    ):
        self._repo = repo
        self._builder = builder
        self._store = vector_store

    async def index(
        self,
        resource_id: UUID,
        *,
        force_recreate: bool = False,
    ) -> None:
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
                return

        await self._store.aadd_documents(
            [document],
            ids=[document_id],
        )

    async def index_many(
        self,
        resource_ids: Sequence[UUID],
        *,
        force_recreate: bool = False,
    ) -> None:
        for resource_id in dict.fromkeys(resource_ids):
            await self.index(
                resource_id,
                force_recreate=force_recreate,
            )

from langchain_core.document_loaders import BaseLoader
from langchain_core.documents import Document
from datetime import datetime, timezone

from pydantic import AwareDatetime, BaseModel, Field


class DocumentMetadata(BaseModel):
    document_id: str = Field(min_length=1)
    source: str = Field(
        min_length=1,
        description="Stable blob URI or locator, without temporary credentials",
    )
    title: str = Field(min_length=1)
    description: str | None = None
    category: str | None = None

    filename: str
    filetype: str = Field(
        description="MIME type, e.g. application/pdf",
    )
    size_bytes: int | None = Field(default=None, ge=0)

    creation_date: AwareDatetime | None = None
    last_modified: AwareDatetime
    ingested_at: AwareDatetime = Field(
        default_factory=lambda: datetime.now(timezone.utc),
    )

    version_id: str | None = None
    content_hash: str | None = Field(
        default=None,
        description="Content checksum; define the algorithm, e.g. SHA-256",
    )


class DocumentLoader(BaseLoader):
    def load(self) -> list[Document]:
        return super().load()

import base64
from typing import Self

from document_processing.splitter import PageChunk
from pydantic import BaseModel, Field, field_serializer, model_validator


class PageRange(BaseModel):
    """Zero-based, inclusive page indices in the source PDF."""

    start: int = Field(ge=0, strict=True)
    end: int = Field(ge=0, strict=True)

    @model_validator(mode="after")
    def validate_order(self) -> Self:
        """Reject ranges whose end precedes their start."""
        if self.end < self.start:
            raise ValueError("end must be greater than or equal to start")
        return self


class PageImage(BaseModel):
    content: bytes
    mime_type: str = "image/png"


class PageContent[TContent: BaseModel | str = str](BaseModel):
    page_range: PageRange
    content: TContent


class ExtractionResult[TContent: BaseModel | str = str](BaseModel):
    pages: list[PageContent[TContent]]


class PDFSection[TContent: BaseModel | str = str](BaseModel):
    """Section metadata and the original PDF pages it describes."""

    metadata: TContent
    document: PageChunk

    @field_serializer("document", when_used="json")
    def serialize_document(self, document: PageChunk) -> dict[str, str | int]:
        """Encode PDF bytes as base64 alongside their range and MIME type."""
        return {
            "content": base64.b64encode(document.content).decode("ascii"),
            "start": document.start,
            "end": document.end,
            "mime_type": document.mime_type,
        }

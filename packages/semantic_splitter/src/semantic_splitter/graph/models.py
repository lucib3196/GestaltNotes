from typing import Self

from pydantic import BaseModel, Field, model_validator


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

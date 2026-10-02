from typing import TypeVar

from pydantic import BaseModel, Field, model_validator


class PageRange(BaseModel):
    start: int = Field(ge=0, strict=True)
    end: int = Field(ge=0, strict=True)

    @model_validator(mode="after")
    def validate_order(self):
        if self.end < self.start:
            raise ValueError("end must be greater than or equal to start")
        return self


TContent = TypeVar("TContent", bound=BaseModel)


class PageContent[TContent: BaseModel](BaseModel):
    page_range: PageRange
    content: str | TContent

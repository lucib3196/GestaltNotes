from typing import Literal

from pydantic import BaseModel

SectionType = Literal[
    "derivation",
    "question",
]


class SectionMetadata(BaseModel):
    section: SectionType


class ExtractedItems[T: BaseModel](BaseModel):
    items: list[T]

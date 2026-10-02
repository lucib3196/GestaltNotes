from typing import Generic

from langchain_core.language_models import BaseChatModel
from pydantic import BaseModel, Field

from .models import PageContent, PageImage, TContent


class SegmentationContext(BaseModel, Generic[TContent]):
    model: BaseChatModel
    structured_output: type[TContent] | None = None
    prompt: str = (
        "Separate the pages into distinct documents based on their content. "
        "Return 1-based, inclusive page ranges."
    )


class InputState(BaseModel):
    pages: list[PageImage]  # File path; consider naming this file_path.


class State(InputState, Generic[TContent]):
    extracted: list[PageContent[TContent]] = Field(default_factory=list)

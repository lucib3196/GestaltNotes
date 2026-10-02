from typing import Generic

from langchain_core.language_models import BaseChatModel
from pydantic import BaseModel, Field

from .models import PageContent, TContent


class SegmentationContext(BaseModel, Generic[TContent]):
    model: BaseChatModel | None = None
    structured_output: type[TContent] | None = None
    prompt: str = (
        "Separate the pages into distinct documents based on their content. "
        "Return 1-based, inclusive page ranges."
    )


class InputState(BaseModel):
    file: str  # File path; consider naming this file_path.


class State(InputState, Generic[TContent]):
    extracted: list[PageContent[TContent]] = Field(default_factory=list)

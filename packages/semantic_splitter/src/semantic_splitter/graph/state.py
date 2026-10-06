from pydantic import BaseModel, Field

from semantic_splitter.graph.models import PageContent, PageImage


class InputState(BaseModel):
    pages: list[PageImage]


class State[TContent: BaseModel | str = str](InputState):
    extracted: list[PageContent[TContent]] = Field(default_factory=list)

from importlib.resources import files

from langchain_core.language_models import BaseChatModel
from pydantic import BaseModel

DEFAULT_PROMPT = (
    files("semantic_splitter")
    .joinpath("prompts/default.txt")
    .read_text(encoding="utf-8")
)


class SegmentationContext[TContent: BaseModel | str = str](BaseModel):
    model: BaseChatModel
    structured_output: type[TContent] | None = None
    prompt: str = DEFAULT_PROMPT

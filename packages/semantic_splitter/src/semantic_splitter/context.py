from langchain_core.language_models import BaseChatModel
from pydantic import BaseModel

DEFAULT_PROMPT = """Identify the document's sections.
For each section, return content matching the supplied schema (a descriptive
title when content is a string) and a 0-based, inclusive page_range.
Use positions in the supplied page images and their added page-index labels,
not page numbers printed in the original document.
Include every page on which the section is covered.
"""


class SegmentationContext[TContent: BaseModel | str = str](BaseModel):
    model: BaseChatModel
    structured_output: type[TContent] | None = None
    prompt: str = DEFAULT_PROMPT

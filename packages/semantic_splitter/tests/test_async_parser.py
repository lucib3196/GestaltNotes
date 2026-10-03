import asyncio
from importlib.resources import as_file, files
from typing import Never
from unittest.mock import Mock

import pytest
from langchain_core.language_models import BaseChatModel
from langchain_core.runnables import RunnableLambda
from pydantic import BaseModel

from semantic_splitter.models import PageImage
from semantic_splitter.pdf_section_parser import PDFSectionParser
from semantic_splitter.state import InputState


@pytest.mark.parametrize("structured", [False, True])
def test_async_parser_and_graph_use_async_model(structured: bool) -> None:
    class Metadata(BaseModel):
        title: str

    content = {"title": "Whole document"} if structured else "Whole document"
    calls = []

    def respond(_messages: list) -> dict:
        calls.append("sync")
        return {"pages": [{"page_range": {"start": 0, "end": 2}, "content": content}]}

    async def arespond(_messages: list) -> dict:
        calls.append("async")
        return {"pages": [{"page_range": {"start": 0, "end": 2}, "content": content}]}

    model = Mock(spec=BaseChatModel, profile={})
    model.with_structured_output.return_value = RunnableLambda(respond, afunc=arespond)
    parser = PDFSectionParser(
        model=model, structured_output=Metadata if structured else None
    )
    example = files("semantic_splitter").joinpath("assets/example.pdf")
    with as_file(example) as source:
        original = source.read_bytes()
        sync_sections = parser.parse(source)
        async_sections = asyncio.run(parser.aparse(source))
        assert source.read_bytes() == original
    assert calls == ["sync", "async"]
    assert sync_sections[0].metadata == async_sections[0].metadata
    assert sync_sections[0].document.start == async_sections[0].document.start == 0
    assert sync_sections[0].document.end == async_sections[0].document.end == 2
    output = asyncio.run(
        parser.graph.ainvoke(
            InputState(pages=[PageImage(content=b"image")]), context=parser.context
        )
    )
    assert output["extracted"]
    assert calls == ["sync", "async", "async"]


def test_async_parser_rejects_invalid_range() -> None:
    async def respond(_messages: list) -> dict:
        return {"pages": [{"page_range": {"start": 0, "end": 3}, "content": "Invalid"}]}

    def unexpected_sync(_messages: list) -> Never:
        raise AssertionError("The async parser must use the async model")

    model = Mock(spec=BaseChatModel, profile={})
    model.with_structured_output.return_value = RunnableLambda(
        unexpected_sync, afunc=respond
    )
    example = files("semantic_splitter").joinpath("assets/example.pdf")
    with as_file(example) as source, pytest.raises(ValueError, match="PDF has 3 pages"):
        asyncio.run(PDFSectionParser(model=model).aparse(source))


def test_async_graph_rejects_empty_pages() -> None:
    model = Mock(spec=BaseChatModel, profile={})
    parser = PDFSectionParser(model=model)
    with pytest.raises(ValueError, match="At least one page"):
        asyncio.run(parser.graph.ainvoke(InputState(pages=[]), context=parser.context))
    model.with_structured_output.assert_not_called()

import asyncio
import os
from importlib.resources import as_file, files

import pymupdf
import pytest
from langchain.chat_models import init_chat_model

from semantic_splitter import PDFSectionParser


@pytest.mark.integration
@pytest.mark.parametrize("asynchronous", [False, True])
def test_gemini_parse_example(asynchronous: bool) -> None:
    if not (os.environ.get("GOOGLE_API_KEY") or os.environ.get("GEMINI_API_KEY")):
        pytest.skip("GOOGLE_API_KEY or GEMINI_API_KEY is required")
    model = init_chat_model(
        model_provider="google_genai",
        model="gemini-2.5-flash",
        timeout=60,
        max_retries=1,
    )
    parser = PDFSectionParser(model=model)
    example = files("semantic_splitter").joinpath("assets/example.pdf")
    with as_file(example) as source:
        sections = (
            asyncio.run(parser.aparse(source)) if asynchronous else parser.parse(source)
        )
    assert sections
    covered = set()
    for section in sections:
        assert isinstance(section.metadata, str) and section.metadata.strip()
        assert 0 <= section.document.start <= section.document.end < 3
        covered.update(range(section.document.start, section.document.end + 1))
        with pymupdf.open(stream=section.document.content, filetype="pdf") as document:
            assert (
                document.page_count == section.document.end - section.document.start + 1
            )
    assert covered == {0, 1, 2}

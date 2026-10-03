import base64
from importlib.resources import as_file, files
from io import BytesIO
from pathlib import Path
from typing import Literal
from unittest.mock import Mock

import pymupdf
import pytest
from document_processing.annotator import PDFAnnotator
from document_processing.converter import PDF2ImageConverter
from langchain_core.language_models import BaseChatModel
from langchain_core.runnables import RunnableLambda
from PIL import Image
from pydantic import BaseModel

from semantic_splitter.models import PDFSection
from semantic_splitter.pdf_section_parser import PDFSectionParser


@pytest.mark.parametrize("structured", [False, True])
def test_parse_example_pdf(structured: bool) -> None:
    class Structure(BaseModel):
        section_type: Literal["derivation", "practice_problem", "conceptual"]

    titles = ["Concept: Constant velocity", "Derivation", "Practice problem"]
    section_types = ["conceptual", "derivation", "practice_problem"]
    example = files("semantic_splitter").joinpath("assets/example.pdf")
    with as_file(example) as source:
        original = source.read_bytes()
        expected_images = PDF2ImageConverter().convert(PDFAnnotator().annotate(source))
        model = Mock(spec=BaseChatModel, profile={})

        def respond(messages: list[dict]) -> dict:
            payload = messages[0]["content"]
            assert len(payload) == 4
            actual_images = [
                base64.b64decode(item["image_url"]["url"].split(",", 1)[1])
                for item in payload[1:]
            ]
            # The real graph receives rendered annotated pages in document order.
            assert actual_images == expected_images
            return {
                "pages": [
                    {
                        "page_range": {"start": index, "end": index},
                        "content": (
                            {"section_type": section_types[index]}
                            if structured
                            else titles[index]
                        ),
                    }
                    for index in reversed(range(3))
                ]
            }

        model.with_structured_output.return_value = RunnableLambda(respond)
        parser = (
            PDFSectionParser[Structure](model=model, structured_output=Structure)
            if structured
            else PDFSectionParser(model=model)
        )
        sections = parser.parse(source)
        assert source.read_bytes() == original

    assert len(sections) == 3
    for index, section in enumerate(sections):
        assert (section.document.start, section.document.end) == (index, index)
        if structured:
            assert isinstance(section.metadata, Structure)
            assert section.metadata.section_type == section_types[index]
        else:
            assert section.metadata == titles[index]
        with pymupdf.open(stream=section.document.content, filetype="pdf") as document:
            assert document.page_count == 1
            assert titles[index] in document[0].get_text()
            assert not document[0].get_drawings()
        serialized = section.model_dump(mode="json")
        assert base64.b64decode(serialized["document"]["content"]) == (
            section.document.content
        )
        assert isinstance(section, PDFSection)


def test_converter_accepts_pdf_bytes(tmp_path: Path) -> None:
    example = files("semantic_splitter").joinpath("assets/example.pdf")
    with as_file(example) as source:
        converter = PDF2ImageConverter()
        images = converter.convert(source.read_bytes())
        assert images == converter.convert(source)
        paths = converter.convert_and_save(source.read_bytes(), tmp_path)
        assert [path.name for path in paths] == [
            "page_0.png",
            "page_1.png",
            "page_2.png",
        ]
        assert [path.read_bytes() for path in paths] == images
    assert len(images) == 3
    for data in images:
        with Image.open(BytesIO(data)) as image:
            assert image.format == "PNG"


def test_parse_rejects_out_of_bounds_range() -> None:
    model = Mock(spec=BaseChatModel, profile={})
    model.with_structured_output.return_value = RunnableLambda(
        lambda _: {
            "pages": [{"page_range": {"start": 0, "end": 3}, "content": "Invalid"}]
        }
    )
    example = files("semantic_splitter").joinpath("assets/example.pdf")
    with (
        as_file(example) as source,
        pytest.raises(ValueError, match="PDF has 3 pages"),
    ):
        PDFSectionParser(model=model).parse(source)

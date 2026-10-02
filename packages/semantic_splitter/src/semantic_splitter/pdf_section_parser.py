from pathlib import Path
from typing import Generic
from langchain.chat_models import init_chat_model
from dotenv import load_dotenv
from document_processing.converter import PDF2ImageConverter
from document_processing.splitter import PageChunk, PDFPageSplitter
from langchain_core.language_models import BaseChatModel
from langgraph.graph import END, START, StateGraph
from pydantic import BaseModel
from typing import Literal
from .models import PageContent, PageImage, TContent
from .nodes import analyze
from .state import InputState, SegmentationContext, State
from .utils import to_serializable
from pydantic import BaseModel, field_serializer
import base64
import json

load_dotenv()
DEFAULT_PROMPT = """Identify the document's sections. 
                For each section, return a descriptive title in content 
                and a 0-based, inclusive page_range. 
                Use positions in the supplied page images, 
                not page numbers printed on the document.
            """


class PDFSection(BaseModel, Generic[TContent]):
    metadata: TContent
    document: PageChunk

    @field_serializer("document", when_used="json")
    def serialize_document(self, document: PageChunk) -> dict:
        return {
            "content": base64.b64encode(document.content).decode("ascii"),
            "start": document.start,
            "end": document.end,
            "mime_type": document.mime_type,
        }


class PDFSectionParser:
    def __init__(
        self,
        model: BaseChatModel,
        prompt: str = DEFAULT_PROMPT,
        *,
        converter: PDF2ImageConverter | None = None,
        splitter: PDFPageSplitter | None = None,
        structured_output: type[BaseModel] | None = None,
    ):
        self._converter = converter if converter is not None else PDF2ImageConverter()
        self._splitter = splitter if splitter is not None else PDFPageSplitter()
        self._graph = self._build_graph()
        self._context = SegmentationContext(
            model=model, structured_output=structured_output, prompt=prompt
        )
        self._structured_output = structured_output

    def parse(self, source: str | Path):
        source = Path(source)
        images = self._converter.convert(source)
        if not images:
            raise ValueError("The PDF contains no pages.")
        mime_type = "image/png" if self._converter.extension == "png" else "image/jpeg"
        pages = [PageImage(content=image, mime_type=mime_type) for image in images]
        output = self._graph.invoke(
            input=InputState(pages=pages),
            context=self._context,
        )
        sections = [PageContent.model_validate(item) for item in output["extracted"]]
        sections.sort(key=lambda section: section.page_range.start)
        return [
            PDFSection(
                metadata=section.content,
                document=self._splitter.extract(
                    source, section.page_range.start, section.page_range.end
                ),
            )
            for section in sections
        ]

    def _build_graph(self):
        builder = StateGraph(
            state_schema=State,
            input_schema=InputState,
            context_schema=SegmentationContext,
        )
        builder.add_node("analyze", analyze)

        builder.add_edge(START, "analyze")
        builder.add_edge("analyze", END)
        return builder.compile()

    @property
    def graph(self):
        return self._graph

    @property
    def context(self):
        return self._context


if __name__ == "__main__":
    file = "/home/lberm/projects/gestalt/GestaltNotes/packages/document_processing/src/document_processing/assets/Lec16_post.pdf"
    model = init_chat_model(
        model_provider="google_genai",
        model="gemini-2.5-flash",
    )

    class Structure(BaseModel):
        section_type : Literal["derivation", "practice_problem", "conceptual"]

    segmenter = PDFSectionParser(
        model,
        prompt="""Identify the document's sections. 
                For each section, return a descriptive title in content 
                and a 0-based, inclusive page_range. 
                Use positions in the supplied page images, 
                not page numbers printed on the document. Ensure to get the whole page range in which the section is being covered""",
        structured_output=Structure,
    )
    content = segmenter.parse(file)
    Path("./output.json").write_text(
        json.dumps(to_serializable(content)),
        encoding="utf-8",
    )

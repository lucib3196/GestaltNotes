import asyncio
from pathlib import Path
from typing import cast

from document_processing.annotator import PDFAnnotator
from document_processing.converter import PDF2ImageConverter
from document_processing.splitter import PDFPageSplitter
from langchain_core.language_models import BaseChatModel
from langchain_core.runnables import RunnableLambda
from langgraph.graph import END, START, StateGraph
from langgraph.graph.state import CompiledStateGraph
from langgraph.runtime import get_runtime
from pydantic import BaseModel

from .context import DEFAULT_PROMPT, SegmentationContext
from .models import PageContent, PageImage, PDFSection
from .nodes import aanalyze, analyze
from .state import InputState, State


def _analyze_pages(state: InputState) -> dict:
    """Run synchronous analysis using the current graph context."""
    return analyze(state, get_runtime(SegmentationContext))


async def _aanalyze_pages(state: InputState) -> dict:
    """Run asynchronous analysis using the current graph context."""
    return await aanalyze(state, get_runtime(SegmentationContext))


class PDFSectionParser[TContent: BaseModel | str = str]:
    """Annotate and analyze PDF pages, then extract the original sections.

    All page ranges are zero-based and inclusive. ``structured_output`` is
    the schema for each section's metadata; omit it to obtain string titles.
    """

    def __init__(
        self,
        model: BaseChatModel,
        prompt: str = DEFAULT_PROMPT,
        *,
        annotator: PDFAnnotator | None = None,
        converter: PDF2ImageConverter | None = None,
        splitter: PDFPageSplitter | None = None,
        structured_output: type[TContent] | None = None,
    ) -> None:
        """Configure the model, metadata schema, and PDF processing tools."""
        self._annotator = annotator if annotator is not None else PDFAnnotator()
        self._converter = converter if converter is not None else PDF2ImageConverter()
        self._splitter = splitter if splitter is not None else PDFPageSplitter()
        self._content_type = cast(type[TContent], structured_output or str)
        self._context = SegmentationContext[self._content_type](
            model=model, structured_output=structured_output, prompt=prompt
        )
        self._graph = self._build_graph()

    def parse(self, source: str | Path) -> list[PDFSection[TContent]]:
        """Identify sections and extract their original PDF pages."""
        source = Path(source)
        pages = self._prepare_pages(source)
        output = self._graph.invoke(
            input=InputState(pages=pages), context=self._context
        )
        return self._extract_sections(source, pages, output["extracted"])

    async def aparse(self, source: str | Path) -> list[PDFSection[TContent]]:
        """Parse asynchronously, moving blocking PDF work to worker threads."""
        source = Path(source)
        pages = await asyncio.to_thread(self._prepare_pages, source)
        output = await self._graph.ainvoke(
            input=InputState(pages=pages), context=self._context
        )
        return await asyncio.to_thread(
            self._extract_sections, source, pages, output["extracted"]
        )

    def _prepare_pages(self, source: Path) -> list[PageImage]:
        """Render annotated pages without overwriting the original PDF."""
        annotated_pdf = self._annotator.annotate(source)
        images = self._converter.convert(annotated_pdf)
        if not images:
            raise ValueError("The PDF contains no pages.")
        mime_type = "image/png" if self._converter.extension == "png" else "image/jpeg"
        return [PageImage(content=image, mime_type=mime_type) for image in images]

    def _extract_sections(
        self, source: Path, pages: list[PageImage], extracted: list
    ) -> list[PDFSection[TContent]]:
        """Validate and sort section ranges, then extract original PDF pages."""
        content_type = self._context.structured_output or str
        sections = [
            PageContent[content_type].model_validate(item) for item in extracted
        ]
        sections.sort(key=lambda section: section.page_range.start)
        for section in sections:
            if section.page_range.end >= len(pages):
                raise ValueError(
                    f"Section ends at page index {section.page_range.end}; "
                    f"the PDF has {len(pages)} pages."
                )
        return [
            PDFSection[content_type](
                metadata=section.content,
                document=self._splitter.extract(
                    source, section.page_range.start, section.page_range.end
                ),
            )
            for section in sections
        ]  # type: ignore

    def _build_graph(
        self,
    ) -> CompiledStateGraph[
        State[TContent], SegmentationContext[TContent], InputState, State[TContent]
    ]:
        """Compile a graph supporting both invoke and ainvoke."""
        builder = StateGraph(
            state_schema=State[self._content_type],
            input_schema=InputState,
            context_schema=SegmentationContext[self._content_type],
        )
        builder.add_node(
            "analyze", RunnableLambda(_analyze_pages, afunc=_aanalyze_pages)
        )
        builder.add_edge(START, "analyze")
        builder.add_edge("analyze", END)
        return builder.compile()

    @property
    def graph(
        self,
    ) -> CompiledStateGraph[
        State[TContent], SegmentationContext[TContent], InputState, State[TContent]
    ]:
        """Return the compiled graph for sync or async execution."""
        return self._graph

    @property
    def context(self) -> SegmentationContext[TContent]:
        """Return the model, prompt, and metadata schema used by the graph."""
        return self._context


if __name__ == "__main__":
    from importlib.resources import as_file, files
    from typing import Literal

    from dotenv import load_dotenv
    from langchain.chat_models import init_chat_model
    from pydantic import TypeAdapter

    load_dotenv()

    class Structure(BaseModel):
        section_type: Literal["derivation", "practice_problem", "conceptual"]

    model = init_chat_model(
        model_provider="google_genai",
        model="gemini-2.5-flash",
    )
    parser = PDFSectionParser[Structure](
        model=model,
        structured_output=Structure,
    )
    example = files("semantic_splitter").joinpath("assets/example.pdf")
    with as_file(example) as source:
        sections = parser.parse(source)

    Path("output.json").write_text(
        TypeAdapter(list[PDFSection[Structure]])
        .dump_json(sections, indent=2)
        .decode("utf-8"),
        encoding="utf-8",
    )

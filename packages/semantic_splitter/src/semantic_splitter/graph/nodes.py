from langgraph.runtime import Runtime
from multimodal_llm import MultiModalLLM
from pydantic import BaseModel

from semantic_splitter.graph.context import SegmentationContext
from semantic_splitter.graph.models import ExtractionResult, PageContent
from semantic_splitter.graph.state import InputState


def analyze[TContent: BaseModel | str](
    state: InputState,
    runtime: Runtime[SegmentationContext[TContent]],
) -> dict[str, list[PageContent[TContent]]]:
    """Analyze page images synchronously and return section metadata."""
    if not state.pages:
        raise ValueError("At least one page is required.")

    llm = MultiModalLLM(runtime.context.model)

    content_type = runtime.context.structured_output
    if content_type is None:
        content_type = str

    output_model = ExtractionResult[content_type]

    result = llm.invoke(
        prompt=runtime.context.prompt,
        images=[page.content for page in state.pages],
        mime_type=state.pages[0].mime_type,
        output_model=output_model,
    )
    result = ExtractionResult[content_type].model_validate(result)
    return {"extracted": result.pages}  # type: ignore


async def aanalyze[TContent: BaseModel | str](
    state: InputState,
    runtime: Runtime[SegmentationContext[TContent]],
) -> dict[str, list[PageContent[TContent]]]:
    """Analyze page images asynchronously and return section metadata."""
    if not state.pages:
        raise ValueError("At least one page is required.")

    llm = MultiModalLLM(runtime.context.model)

    content_type = runtime.context.structured_output
    if content_type is None:
        content_type = str

    output_model = ExtractionResult[content_type]

    result = await llm.ainvoke(
        prompt=runtime.context.prompt,
        images=[page.content for page in state.pages],
        mime_type=state.pages[0].mime_type,
        output_model=output_model,
    )
    result = ExtractionResult[content_type].model_validate(result)
    return {"extracted": result.pages}  # type: ignore

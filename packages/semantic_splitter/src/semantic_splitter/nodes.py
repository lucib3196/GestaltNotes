from langgraph.runtime import Runtime
from multimodal_llm import MultiModalLLM

from .models import ExtractionResult
from .state import InputState, SegmentationContext


def analyze(
    state: InputState,
    runtime: Runtime[SegmentationContext],
):
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
    return {"extracted": result.pages}

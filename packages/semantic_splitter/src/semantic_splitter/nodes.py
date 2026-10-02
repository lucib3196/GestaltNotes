from langgraph.runtime import Runtime
from multimodal_llm import MultiModalLLM
from .state import SegmentationContext, State, InputState


def analyze(state: InputState, runtime: Runtime[SegmentationContext]) -> None:
    print("Analyzing Document... ")
    llm = MultiModalLLM(runtime.context.model)
    result = llm.invoke(
        prompt=runtime.context.prompt,
        images=[p.content for p in state.pages],
        mime_type=state.pages[0].mime_type,
        output_model=runtime.context.structured_output,
    )
    print(result)


def chunk(state: State, runtime: Runtime[SegmentationContext]) -> None:
    print("Chunking Pages..")


def finalize(state: State, runtime: Runtime[SegmentationContext]) -> None:
    print("Finalizing....")

from pathlib import Path

from langchain_core.runnables import RunnableConfig

from lecture_processor.graph.context import ExtractionContext
from lecture_processor.graph.graph import build_graph
from lecture_processor.graph.state import InputState, OutputState


def process_lecture(
    source: str | Path,
    *,
    context: ExtractionContext,
    config: RunnableConfig | None = None,
) -> OutputState:
    """Process a lecture using the supplied graph and runtime configuration."""

    graph = build_graph(max_attempts=context.failure.max_attempts)
    result = graph.invoke(
        InputState(source=source),
        context=context,
        config=config,
    )
    return OutputState.model_validate(result)

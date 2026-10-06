from langgraph.graph import END, START, StateGraph

from .content_generation import (
    CONTENT_GENERATION_NODES,
    LECTURE_PREPARATION_NODES,
)
from .context import ExtractionContext
from .error_handling import handle_node_error, retry_policy
from .routers import route_generation, route_sections, route_tasks
from .section_extraction import (
    SECTION_EXTRACTION_NODES,
    SECTION_PREPARATION_NODES,
)
from .state import InputState, OutputState, State


def build_graph(*, max_attempts: int = 3):
    """Build the graph with the requested maximum attempts per node."""
    if max_attempts < 1:
        raise ValueError("max_attempts must be at least 1")
    node_retry_policy = retry_policy._replace(max_attempts=max_attempts)

    builder = StateGraph(
        state_schema=State,
        input_schema=InputState,
        context_schema=ExtractionContext,
        output_schema=OutputState,
    )

    builder.set_node_defaults(error_handler=handle_node_error)  # type: ignore
    for nodes in (
        SECTION_PREPARATION_NODES,
        SECTION_EXTRACTION_NODES,
        LECTURE_PREPARATION_NODES,
        CONTENT_GENERATION_NODES,
    ):
        for name, node in nodes.items():
            builder.add_node(
                name,
                node,
                retry_policy=node_retry_policy,
            )

    builder.add_conditional_edges(
        START,
        route_tasks,
        [*SECTION_PREPARATION_NODES, *LECTURE_PREPARATION_NODES, END],
    )
    builder.add_conditional_edges(
        "extract_sections",
        route_sections,
        [*SECTION_EXTRACTION_NODES, END],
    )
    builder.add_conditional_edges(
        "prepare_lecture",
        route_generation,
        [*CONTENT_GENERATION_NODES, END],
    )

    for name in (*SECTION_EXTRACTION_NODES, *CONTENT_GENERATION_NODES):
        builder.add_edge(name, END)

    return builder.compile()


graph = build_graph()

if __name__ == "__main__":
    import json
    from pathlib import Path

    from dotenv import load_dotenv
    from langchain.chat_models import init_chat_model
    from semantic_splitter.utils import to_serializable

    from lecture_processor.utils import save_graph_visualization

    save_graph_visualization(graph, "assets")  # type: ignore

    load_dotenv()

    file = Path(
        r"/home/lberm/projects/gestalt/GestaltNotes/packages/document_processing/src/document_processing/assets/output.pdf"
    ).resolve()
    model = init_chat_model(
        model_provider="google_genai",
        model="gemini-2.5-flash",
    )
    result = graph.invoke(
        InputState(source=file),
        context=ExtractionContext(
            model=model,
        ),
    )
    Path("./full_output.json").write_text(json.dumps(to_serializable(result)))

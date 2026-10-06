from pathlib import Path

from langchain_core.runnables.graph import CurveStyle, NodeStyles
from langgraph.graph.state import CompiledStateGraph

NODE_LABELS = {
    "__start__": "Start",
    "__end__": "Complete",
    "prepare_lecture": "Render full lecture",
    "extract_sections": "Identify sections",
    "extract_derivations": "Extract derivations",
    "extract_questions": "Extract worked questions",
    "generate_conceptual_questions": "Generate conceptual questions",
    "generate_lecture_summary": "Generate lecture summary",
}

NODE_COLORS = NodeStyles(
    default=(
        "fill:#f1f5f9,stroke:#64748b,stroke-width:1.5px,"
        "color:#0f172a,line-height:1.6"
    ),
    first=(
        "fill:#eff6ff,stroke:#3b82f6,stroke-width:2px,"
        "color:#1e3a8a,line-height:1.6"
    ),
    last=(
        "fill:#ecfdf5,stroke:#10b981,stroke-width:2px,"
        "color:#064e3b,line-height:1.6"
    ),
)


def save_graph_visualization(
    graph: CompiledStateGraph,
    folder_path: str | Path,
    filename: str = "graph.png",
) -> None:
    """Save a graph PNG with readable task and recovery labels."""
    diagram = graph.get_graph()

    for node_id, node in list(diagram.nodes.items()):
        label = NODE_LABELS.get(node_id)

        if node_id == "__default_error_handler__":
            label = "Handle task failure"
        elif node_id.startswith("__error_handler__"):
            task_id = node_id.removeprefix("__error_handler__")
            task_label = NODE_LABELS.get(task_id, task_id.replace("_", " "))
            label = f"Handle failure: {task_label}"

        if label is not None:
            diagram.nodes[node_id] = node.copy(name=label)

    image_bytes = diagram.draw_mermaid_png(
        node_colors=NODE_COLORS,
        curve_style=CurveStyle.LINEAR,
        wrap_label_n_words=4,
        # background_color="#ffffff",
        padding=32,
    )

    save_path = Path(folder_path) / filename
    save_path.parent.mkdir(parents=True, exist_ok=True)
    save_path.write_bytes(image_bytes)
    print(f"Saved graph visualization at: {save_path}")

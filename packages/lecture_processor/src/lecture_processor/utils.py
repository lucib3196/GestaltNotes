from langgraph.graph.state import CompiledStateGraph
from typing import Any
from pathlib import Path


def save_graph_visualization(
    graph: CompiledStateGraph | Any,
    folder_path: str | Path,
    filename: str = "graph.png",
) -> None:
    """Render a graph visualization to PNG and save it to disk."""
    try:
        image_bytes = graph.get_graph().draw_mermaid_png()
        Path(folder_path).mkdir(exist_ok=True)
        save_path = Path(folder_path) / filename
        save_path.write_bytes(image_bytes)
        print(f"Saved graph visualization at: {save_path}")
    except ValueError:
        raise
    except Exception as error:
        print(f"Graph visualization failed: {error}")

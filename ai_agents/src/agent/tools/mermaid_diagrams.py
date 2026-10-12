from typing import Any

from langchain.tools import ToolRuntime, tool
from agent.models.flow_diagram import FlowDiagram, MermaidArtifact
from agent.tools.diagram_summary import summarize_diagram

from agent.middlewear.model_routing import ConfigSchema, get_model


@tool(
    response_format="content_and_artifact",
    description=(
        "Create a visual flow diagram explaining concepts, derivation steps, "
        "processes, or relationships. Provide a focused query describing "
        "what should be illustrated."
    ),
    return_direct=True,
)
async def create_mermaid_diagram(
    query: str,
    runtime: ToolRuntime[ConfigSchema],
) -> tuple[str, dict[str, Any]]:
    """Create a Mermaid diagram to illustrate a process or relationships."""
    model = get_model(runtime.context.model)
    diagram = await model.with_structured_output(FlowDiagram).ainvoke(
        [
            (
                "system",
                "Create a clear educational flow diagram for the student's request. "
                "Use concise node labels and unique node IDs. "
                "Every edge must reference an existing node ID. "
                "Use arrow labels for brief relationships and descriptions for "
                "additional explanations of how the nodes relate. "
                "Prefer a small, readable diagram over an exhaustive one. "
                "For derivations, connect steps in logical order and explain "
                "the principle or transformation connecting them. "
                "Do not invent physical relationships.",
            ),
            ("human", query),
        ]
    )
    diagram = FlowDiagram.model_validate(diagram)
    summary = await summarize_diagram(model, diagram)
    artifact = MermaidArtifact(data=diagram)
    return summary, artifact.model_dump(mode="json")

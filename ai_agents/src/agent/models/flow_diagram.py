from typing import Annotated, Literal

from pydantic import BaseModel, Field, model_validator

HexColor = Annotated[str, Field(pattern=r"^#[0-9A-Fa-f]{6}$")]


class DiagramNode(BaseModel):
    id: str = Field(
        description="Unique identifier used to reference this node in relationships."
    )
    label: str = Field(description="Short, readable text displayed inside the node.")
    color: HexColor | None = Field(
        default=None, description="Optional six-digit hex node background color."
    )
    assessment: (
        Literal["strength", "needs_practice", "insufficient_evidence"] | None
    ) = Field(
        default=None,
        description="Quiz assessment of this concept; omit for general diagrams.",
    )


class DiagramEdge(BaseModel):
    color: HexColor | None = Field(
        default=None, description="Optional six-digit hex relationship line color."
    )
    source: str = Field(
        description="Identifier of the node where the relationship starts."
    )
    target: str = Field(
        description="Identifier of the node where the relationship ends."
    )
    label: str | None = Field(
        default=None,
        description="Short relationship label displayed on the connecting arrow.",
    )
    description: str | None = Field(
        default=None,
        description=(
            "Additional information explaining how the source node relates "
            "to the target node, including the reason or meaning of the connection."
        ),
    )


class DiagramLegendItem(BaseModel):
    label: str = Field(description="Readable explanation of the color's meaning.")
    color: HexColor = Field(description="Six-digit hex color used in the diagram.")


class FlowDiagram(BaseModel):
    legend: list[DiagramLegendItem] = Field(
        default_factory=list,
        description="Color meanings displayed alongside the diagram.",
    )
    title: str = Field(
        description="A concise title describing what the diagram illustrates."
    )
    direction: Literal["LR", "TD"] = Field(
        default="TD",
        description="Layout direction: LR for left to right, TD for top to bottom.",
    )
    nodes: list[DiagramNode] = Field(
        min_length=1,
        description="Concepts or steps represented in the diagram.",
    )
    edges: list[DiagramEdge] = Field(
        default_factory=list,
        description="Relationships connecting nodes by their identifiers.",
    )

    @model_validator(mode="after")
    def validate_relationships(self) -> "FlowDiagram":
        node_ids = [node.id for node in self.nodes]
        if len(node_ids) != len(set(node_ids)):
            raise ValueError("Diagram node IDs must be unique.")
        known_ids = set(node_ids)
        if any(
            edge.source not in known_ids or edge.target not in known_ids
            for edge in self.edges
        ):
            raise ValueError("Diagram edges must reference existing nodes.")
        return self

    def to_str(self) -> str:
        """Serialize the graph for a subsequent explanation prompt."""
        return self.model_dump_json(indent=2)


class MermaidArtifact(BaseModel):
    kind: Literal["mermaid"] = Field(
        default="mermaid", description="Diagram artifact kind."
    )
    data: FlowDiagram = Field(description="The generated nodes and relationships.")

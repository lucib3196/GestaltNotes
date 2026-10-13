import re
from typing import Annotated, Literal

from pydantic import BaseModel, Field, field_validator, model_validator

HexColor = Annotated[str, Field(pattern=r"^#[0-9A-Fa-f]{6}$")]

EdgeType = Literal[
    "-->",  # Solid arrow
    "---",  # Solid line
    "-.->",  # Dotted arrow
    "-.-",  # Dotted line
    "==>",  # Thick arrow
    "===",  # Thick line
    "~~~",  # Invisible connection
    "--o",  # Circle endpoint
    "--x",  # Cross endpoint
    "<-->",  # Arrows at both ends
    "o--o",  # Circles at both ends
    "x--x",  # Crosses at both ends
]


class DiagramNode(BaseModel):
    id: str = Field(
        pattern=r"^[A-Za-z_][A-Za-z0-9_]*$",
        description="Unique Mermaid-safe identifier for this node.",
    )
    shape: str = Field(default="rect")
    label: str = Field(description="Short, readable text displayed inside the node.")
    description: str | None = Field(
        default=None, description="A short description to explain the concept further "
    )
    color: HexColor | None = Field(
        default=None,
        description="Optional six-digit hex background color.",
    )
    border_color: HexColor | None = Field(
        default=None,
        description="Optional six-digit hex border color.",
    )
    text_color: HexColor | None = Field(
        default=None,
        description="Optional six-digit hex text color.",
    )
    border_width: float | None = Field(
        default=None,
        ge=0,
        le=10,
        description="Optional border width in pixels.",
    )

    @field_validator("id")
    @classmethod
    def validate_id(cls, value: str) -> str:
        if value == "end":
            raise ValueError("'end' is reserved by Mermaid.")
        return value

    # @field_validator("shape")
    # @classmethod
    # def normalize_shape(cls, value: str) -> str:
    #     # Expand this set to match your installed Mermaid version.
    #     supported = {
    #         "rect",
    #         "rounded",
    #         "stadium",
    #         "diam",
    #         "cyl",
    #         "doc",
    #         "lean-r",
    #         "fr-rect",
    #     }
    #     value = value.strip().lower()
    #     return value if value in supported else "rect"

    def code(self) -> str:
        # Encode characters that could interfere with Mermaid syntax.
        label = re.sub(
            r'[&"#<>]',
            lambda match: f"#{ord(match.group())};",
            " ".join(self.label.splitlines()).replace("\\", "\\\\"),
        )
        return f'{self.id}@{{ shape: {self.shape}, label: "{label}" }}'

    def style(self) -> str:
        styles: list[str] = []

        if self.color is not None:
            styles.append(f"fill:{self.color}")
        if self.border_color is not None:
            styles.append(f"stroke:{self.border_color}")
        if self.text_color is not None:
            styles.append(f"color:{self.text_color}")
        if self.border_width is not None:
            styles.append(f"stroke-width:{self.border_width:g}px")

        return f"style {self.id} {','.join(styles)}" if styles else ""


class DiagramEdge(BaseModel):
    source: str = Field(
        pattern=r"^[A-Za-z_][A-Za-z0-9_]*$",
        description="ID of the source node.",
    )
    target: str = Field(
        pattern=r"^[A-Za-z_][A-Za-z0-9_]*$",
        description="ID of the target node.",
    )
    edge_type: EdgeType = Field(
        default="-->",
        description="Mermaid connection type.",
    )
    label: str | None = Field(
        default=None,
        description="Short text displayed on the connection.",
    )
    color: HexColor | None = Field(
        default=None,
        description="Optional six-digit hex line color.",
    )
    width: float | None = Field(
        default=None,
        ge=0,
        le=10,
        description="Optional line width in pixels.",
    )

    def code(self) -> str:
        label_code = ""

        if self.label and self.edge_type != "~~~":
            label = re.sub(
                r'[&"#<>|]',
                lambda match: f"#{ord(match.group())};",
                " ".join(self.label.splitlines()),
            )
            label_code = f'|"{label}"|'

        return f"{self.source} {self.edge_type}{label_code} {self.target}"

    def style(self, index: int) -> str:
        if index < 0:
            raise ValueError("Edge index must be non-negative.")

        if self.edge_type == "~~~":
            return ""

        styles: list[str] = []

        if self.color is not None:
            styles.append(f"stroke:{self.color}")
        if self.width is not None:
            styles.append(f"stroke-width:{self.width:g}px")

        return f"linkStyle {index} {','.join(styles)}" if styles else ""


class FlowDiagram(BaseModel):
    legend: list[DiagramNode] | None = Field(
        default_factory=list,
        description="An optional legend useful when nodes represent specific information",
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
        legend_ids = [node.id for node in (self.legend or [])]
        if len(legend_ids) != len(set(legend_ids)):
            raise ValueError("Legend node IDs must be unique.")
        if known_ids.intersection(legend_ids):
            raise ValueError("Legend node IDs must differ from diagram node IDs.")
        if any(
            edge.source not in known_ids or edge.target not in known_ids
            for edge in self.edges
        ):
            raise ValueError("Diagram edges must reference existing nodes.")
        return self

    def serialize(self) -> str:
        """Serialize the graph for a subsequent explanation prompt."""
        return self.model_dump_json(indent=2)

    def code(self) -> str:
        node_mapping = {node.id: node for node in self.nodes}

        if len(node_mapping) != len(self.nodes):
            raise ValueError("Node IDs must be unique.")

        lines = [f"flowchart {self.direction}"]

        # Include all nodes, even those without edges.
        lines.extend(node.code() for node in self.nodes)

        for edge in self.edges:
            if edge.source not in node_mapping:
                raise ValueError(f"Unknown source node: {edge.source}")
            if edge.target not in node_mapping:
                raise ValueError(f"Unknown target node: {edge.target}")

            lines.append(edge.code())

        for node in self.nodes:
            style = node.style()
            if style:
                lines.append(style)

        for index, edge in enumerate(self.edges):
            style = edge.style(index)
            if style:
                lines.append(style)

        if self.legend:
            used_ids = set(node_mapping)
            used_ids.update(node.id for node in self.legend)

            legend_id = "diagram_legend"
            while legend_id in used_ids:
                legend_id += "_"

            lines.extend(
                [
                    f'subgraph {legend_id}["Legend"]',
                    "direction LR",
                ]
            )
            lines.extend(node.code() for node in self.legend)
            lines.append("end")

            for node in self.legend:
                style = node.style()
                if style:
                    lines.append(style)

        return "\n".join(lines)


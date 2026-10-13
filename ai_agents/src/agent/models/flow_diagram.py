from pydantic import BaseModel, Field
from typing import Literal


class MermaidData(BaseModel):
    title: str
    code: str


class MermaidArtifact(BaseModel):
    kind: Literal["mermaid"] = Field(
        default="mermaid", description="Diagram artifact kind."
    )
    data: MermaidData

from typing import Literal

from pydantic import BaseModel, Field


class MermaidData(BaseModel):
    title: str
    code: str


class MermaidArtifact(BaseModel):
    kind: Literal["mermaid"] = Field(
        default="mermaid", description="Diagram artifact kind."
    )
    data: MermaidData

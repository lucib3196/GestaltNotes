from typing import Literal

from pydantic import BaseModel, Field


class LectureAnalysis(BaseModel):
    title: str = Field(description="Concise title reflecting the lecture content.")
    summary: str = Field(
        description="Brief explanation of the main ideas and how they connect."
    )
    topics: list[str] = Field(
        description="Primary topics expressed as short noun phrases."
    )
    objectives: list[str] = Field(
        description=(
            "Capabilities supported by the lecture content, each starting "
            "with an action verb. Do not invent unsupported objectives."
        )
    )
    prerequisites: list[str] = Field(
        description=(
            "Prior knowledge explicitly stated or clearly required by the "
            "material; [] if none can be identified."
        )
    )
    kind: Literal["conceptual", "derivation", "computational", "mixed"] = Field(
        description="Primary teaching emphasis of the lecture."
    )

    def as_string(self) -> str:
        parts = [
            f"## {self.title}",
            f"**Type:** {self.kind}",
            f"### Summary\n\n{self.summary}",
        ]
        for heading, items in (
            ("Topics", self.topics),
            ("Learning Objectives", self.objectives),
            ("Prerequisites", self.prerequisites),
        ):
            if items:
                parts.append(
                    f"### {heading}\n\n" + "\n".join(f"- {item}" for item in items)
                )
        return "\n\n".join(parts) + "\n"

from typing import Literal

from pydantic import BaseModel, Field
from semantic_splitter.graph.models import PageRange

QuestionType = Literal[
    "conceptual",
    "computational",
    "derivation",
    "multiple_choice",
    "short_answer",
    "mixed",
]


class Option(BaseModel):
    label: str | None = Field(
        description="Source option label, such as A or B; null if absent."
    )
    text: str = Field(description="Answer option as written in the source.")
    is_correct: bool | None = Field(
        description="Whether the source identifies this as correct; null if unknown."
    )

    def as_string(self) -> str:
        label = f"{self.label}. " if self.label else ""
        marker = "✅ " if self.is_correct is True else ""
        return f"- {marker}{label}{self.text}"


class SolutionStep(BaseModel):
    explanation: str = Field(
        description="Source-supported action or reasoning in this step."
    )
    equation: str | None = Field(
        description="Equation in LaTeX without delimiters; null if absent."
    )
    reference: PageRange | None = Field(
        description="Zero-based, inclusive source pages; null if unavailable."
    )

    def as_string(self) -> str:
        parts = [self.explanation]
        if self.equation is not None:
            parts.append(f"$$\n{self.equation}\n$$")
        if self.reference is not None:
            parts.append(f"**Reference:** {self.reference}")
        return "\n\n".join(parts)


class ExtractedQuestion(BaseModel):
    question: str = Field(
        description=(
            "Full source question, including given values, units, and subparts. "
            "Describe essential diagram information when present."
        )
    )
    kind: QuestionType = Field(description="Best-fitting question category.")
    topics: list[str] = Field(
        description="Relevant topic names; [] if none can be identified."
    )
    options: list[Option] = Field(
        description="Source answer options; [] when none are present."
    )
    solution: list[SolutionStep] = Field(
        description=(
            "Solution steps shown in the source, in order. "
            "Do not reconstruct missing work; [] if no solution is shown."
        )
    )
    answer: str | None = Field(
        description=(
            "Final answer stated in the source, including units or conditions; "
            "null if absent."
        )
    )
    gaps: list[str] = Field(
        description="Missing or unreadable solution information; [] if none."
    )
    reference: PageRange | None = Field(
        description="Zero-based, inclusive source pages; null if unavailable."
    )

    def as_string(self) -> str:
        parts = [
            "### Extracted Question",
            f"**Type:** {self.kind}",
            self.question,
        ]
        if self.topics:
            parts.append(f"**Topics:** {', '.join(self.topics)}")
        if self.options:
            parts.append(
                "**Options:**\n\n"
                + "\n".join(option.as_string() for option in self.options)
            )
        if self.solution:
            parts.append("**Solution:**")
            parts.extend(
                f"#### Step {index}\n\n{step.as_string()}"
                for index, step in enumerate(self.solution, start=1)
            )
        if self.answer is not None:
            parts.append(f"**Answer:** {self.answer}")
        if self.gaps:
            parts.append("**Gaps:**\n\n" + "\n".join(f"- {gap}" for gap in self.gaps))
        if self.reference is not None:
            parts.append(f"**Reference:** {self.reference}")
        return "\n\n".join(parts) + "\n"

from typing import Literal

from pydantic import BaseModel, Field
from semantic_splitter.graph.models import PageRange


class SymbolDefinition(BaseModel):
    symbol: str = Field(description="Symbol written in LaTeX.")
    meaning: str = Field(
        description="Meaning stated in the lecture; do not invent definitions."
    )


class DerivationStep(BaseModel):
    equation_latex: str | None = Field(
        description=(
            "Equation or transformation shown in this step, in LaTeX "
            "without delimiters. Null for a purely verbal step."
        )
    )
    explanation: str = Field(
        description="Explain the mathematical action presented in this step."
    )
    rule_used: str | None = Field(
        description=(
            "Named law, identity, theorem, or algebraic operation supporting "
            "this step. Null if it cannot be identified from the source."
        )
    )
    reference: PageRange = Field(
        description="Zero-based, inclusive source PDF page indices."
    )

    def as_string(self) -> str:
        """Render this step as Markdown with one-based PDF page numbers."""
        lines = [self.explanation]

        if self.equation_latex is not None:
            lines.extend(["", "$$", self.equation_latex, "$$", ""])

        if self.rule_used is not None:
            lines.append(f"**Rule:** {self.rule_used}")

        # lines.append(f"**Source evidence:** {self.source_evidence}")

        start = self.reference.start + 1
        end = self.reference.end + 1
        pages = f"Page {start}" if start == end else f"Pages {start}–{end}"
        lines.append(f"**Reference:** {pages}")

        return "\n".join(lines)


class Derivation(BaseModel):
    title: str = Field(
        description="Concise name of the derivation.",
    )
    description: str = Field(
        description="What is being derived and its purpose in the lecture.",
    )
    assumptions: list[str] = Field(
        description=(
            "Assumptions, approximations, and validity conditions explicitly "
            "stated in the source. Return [] if none are stated."
        )
    )
    symbols: list[SymbolDefinition] = Field(
        description="Symbols explicitly defined in the source; [] if none."
    )
    steps: list[DerivationStep] = Field(
        description=(
            "Source-supported mathematical and logical steps in source order. "
            "Preserve intermediate equations; do not fill omitted steps."
        )
    )
    result_latex: str | None = Field(
        description=(
            "Final expression explicitly reached in the source, in LaTeX "
            "without delimiters. Null if no final expression is shown."
        )
    )
    completeness: Literal["complete", "partial", "unclear"] = Field(
        description=(
            "complete: the source presents a connected derivation; "
            "partial: it omits steps or stops before the result; "
            "unclear: unreadable or ambiguous material prevents assessment."
        )
    )
    gaps: list[str] = Field(
        description=(
            "Describe skipped transitions, unreadable equations, or missing "
            "conditions. Do not solve them. Return [] when none are observed."
        )
    )
    reference: PageRange = Field(
        description="Zero-based, inclusive pages containing this derivation.",
    )

    def as_string(self) -> str:
        """Render the extraction as Markdown with one-based PDF page numbers."""

        lines = [
            f"### **{self.title}**",
            "",
            f"**Description:** {self.description}",
            "",
            f"**Completeness:** {self.completeness}",
        ]
        if self.assumptions:
            lines.extend(["", "**Assumptions:**", ""])
            lines.extend(f"- $${assumption}$$" for assumption in self.assumptions)
        if self.symbols:
            lines.extend(["", "**Symbols:**", ""])
            lines.extend(
                f"- ${symbol.symbol}$: {symbol.meaning}" for symbol in self.symbols
            )
        lines.extend(["", "**Steps:**", ""])
        if not self.steps:
            lines.append("No source-supported steps were extracted.")
        for index, step in enumerate(self.steps, start=1):
            lines.extend(
                [
                    f"#### Step {index}",
                    "",
                    step.as_string(),
                    "",
                ]
            )
        if self.result_latex is not None:
            lines.extend(["", "**Result:**", "", "$$", self.result_latex, "$$"])
        if self.gaps:
            lines.extend(["", "**Gaps:**", ""])
            lines.extend(f"- {gap}" for gap in self.gaps)
        return "\n".join(lines) + "\n"


class LectureDerivations(BaseModel):
    derivations: list[Derivation] = Field(
        description=(
            "Every distinct derivation in the supplied lecture material. "
            "Return [] when no derivations are present."
        )
    )

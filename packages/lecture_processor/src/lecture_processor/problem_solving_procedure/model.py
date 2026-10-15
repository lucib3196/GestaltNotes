from pydantic import BaseModel, Field
from semantic_splitter.graph.models import PageRange


class ProcedureStep(BaseModel):
    action: str = Field(description="Instruction describing what to do.")
    rationale: str | None = Field(
        description="Source-supported reason for this action; null if absent."
    )
    equations: list[str] = Field(
        description="Relevant equations in LaTeX without delimiters; [] if none."
    )
    checks: list[str] = Field(
        description=(
            "Source-supported checks, such as units, signs, or limiting cases; "
            "[] if none."
        )
    )

    def as_string(self) -> str:
        parts = [self.action]
        if self.rationale is not None:
            parts.append(f"**Why:** {self.rationale}")
        parts.extend(f"$$\n{equation}\n$$" for equation in self.equations)
        if self.checks:
            parts.append(
                "**Checks:**\n\n" + "\n".join(f"- {check}" for check in self.checks)
            )
        return "\n\n".join(parts)


class ProblemSolvingProcedure(BaseModel):
    title: str = Field(description="Concise name of the problem-solving method.")
    purpose: str = Field(description="Type of problem this procedure solves.")
    applicability: list[str] = Field(
        description="Source-supported assumptions and conditions for using it."
    )
    inputs: list[str] = Field(
        description="Required quantities or information, including units if stated."
    )
    steps: list[ProcedureStep] = Field(
        description=(
            "Ordered, reusable steps taught explicitly or demonstrated by "
            "worked examples. Preserve source-supported reasoning."
        )
    )
    limitations: list[str] = Field(
        description="Restrictions or failure cases stated in the source; [] if none."
    )
    reference: PageRange = Field(
        description="Zero-based, inclusive pages supporting this procedure."
    )

    def as_string(self) -> str:
        parts = [f"### {self.title}", f"**Purpose:** {self.purpose}"]
        for heading, items in (
            ("Applicability", self.applicability),
            ("Inputs", self.inputs),
        ):
            if items:
                parts.append(
                    f"**{heading}:**\n\n" + "\n".join(f"- {item}" for item in items)
                )
        parts.extend(
            f"#### Step {index}\n\n{step.as_string()}"
            for index, step in enumerate(self.steps, start=1)
        )
        if self.limitations:
            parts.append(
                "**Limitations:**\n\n"
                + "\n".join(f"- {item}" for item in self.limitations)
            )
        parts.append(f"**Reference:** {self.reference}")
        return "\n\n".join(parts) + "\n"

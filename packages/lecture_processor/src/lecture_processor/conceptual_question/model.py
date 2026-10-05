from pydantic import BaseModel, Field
from semantic_splitter.graph.models import PageRange

from lecture_processor.extracted_question.model import Option


class ConceptualQuestion(BaseModel):
    question: str = Field(description="Conceptual question stated in the source.")
    topics: list[str] = Field(
        description="Relevant concepts; do not force a fixed number of topics."
    )
    options: list[Option] = Field(
        description="Source answer options; [] for an open-ended question."
    )
    answer: str | None = Field(
        description="Source-supported answer; null if not provided."
    )
    explanation: str | None = Field(
        description=(
            "Source-supported physical or conceptual reasoning for the answer; "
            "null if absent. Do not invent an explanation."
        )
    )
    reference: PageRange | None = Field(
        description="Zero-based, inclusive source pages; null if unavailable."
    )

    def as_string(self) -> str:
        parts = ["### Conceptual Question", self.question]
        if self.topics:
            parts.append(f"**Topics:** {', '.join(self.topics)}")
        if self.options:
            parts.append(
                "**Options:**\n\n"
                + "\n".join(option.as_string() for option in self.options)
            )
        if self.answer is not None:
            parts.append(f"**Answer:** {self.answer}")
        if self.explanation is not None:
            parts.append(f"**Explanation:** {self.explanation}")
        if self.reference is not None:
            parts.append(f"**Reference:** {self.reference}")
        return "\n\n".join(parts) + "\n"

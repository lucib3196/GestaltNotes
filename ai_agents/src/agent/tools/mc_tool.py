"""Package generated multiple-choice questions using shared models."""

from typing import Annotated, Literal

from gestalt_models import MultipleChoiceQuestion, MultipleChoiceQuestionSet
from langchain.tools import tool
from pydantic import BaseModel, Field


class MultipleChoiceArtifact(BaseModel):
    """Wrap multiple-choice data for application rendering."""

    kind: Literal["multiple-choice-question"] = "multiple-choice-question"
    schema_version: Literal[2] = 2
    data: MultipleChoiceQuestionSet


@tool(return_direct=True, response_format="content_and_artifact")
def create_multiple_choice_questions(
    num_questions: Annotated[
        int, Field(ge=1, description="Number of questions requested by the user.")
    ],
    questions: list[MultipleChoiceQuestion],
) -> tuple[str, dict]:
    """Package exactly the requested number of multiple-choice questions."""
    result = MultipleChoiceQuestionSet(questions=questions)
    artifact = MultipleChoiceArtifact(data=result)
    if len(result.questions) != num_questions:
        raise ValueError(f"Expected exactly {num_questions} questions.")
    return (
        f"Created {len(result.questions)} questions. Feel free to try them out!",
        artifact.model_dump(mode="json"),
    )

"""Package generated multiple-choice questions using shared models."""

from pathlib import Path
from typing import Annotated, Literal

from gestalt_models import MultipleChoiceQuestion, MultipleChoiceQuestionSet
from langchain.tools import tool
from pydantic import BaseModel, Field

MC_QUESTION_PROMPT = (
    Path(__file__).resolve().parents[1] / "prompts" / "mc_question_prompt.md"
).read_text(encoding="utf-8")


class MultipleChoiceArtifact(BaseModel):
    """Wrap multiple-choice data for application rendering."""

    kind: Literal["multiple-choice-question"] = "multiple-choice-question"
    schema_version: Literal[2] = 2
    data: MultipleChoiceQuestionSet


@tool(
    description=MC_QUESTION_PROMPT,
    return_direct=True,
    response_format="content_and_artifact",
)
def create_multiple_choice_questions(
    num_questions: Annotated[
        int, Field(ge=1, description="Number of questions requested by the user.")
    ],
    quiz_title: Annotated[
        str, Field(min_length=1, description="A concise title identifying the quiz topic.")
    ],
    description: Annotated[
        str,
        Field(
            min_length=1,
            description="One or two sentences describing the concepts assessed.",
        ),
    ],
    questions: list[MultipleChoiceQuestion],
) -> tuple[str, dict]:
    """Package generated questions into a multiple-choice artifact."""
    result = MultipleChoiceQuestionSet(
        quiz_title=quiz_title,
        description=description,
        questions=questions,
    )
    artifact = MultipleChoiceArtifact(data=result)
    if len(result.questions) != num_questions:
        raise ValueError(f"Expected exactly {num_questions} questions.")
    return (
        f"Created {len(result.questions)} questions. Feel free to try them out!",
        artifact.model_dump(mode="json"),
    )

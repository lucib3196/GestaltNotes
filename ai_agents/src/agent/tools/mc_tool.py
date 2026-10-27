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
    r"""Package exactly the requested number of multiple-choice questions.

    Prepare all questions before calling this tool. Follow these rules:

    Structure and quality:
    - Generate exactly num_questions questions about the requested topic.
    - Give each question exactly four distinct options and one correct answer.
    - Set correct_answer_index to the correct option's zero-based index, 0–3.
    - State the necessary givens, units, and assumptions.
    - Use plausible distractors based on common conceptual or calculation errors.
    - Keep the answer and explanation consistent with the question's givens.

    Formatting:
    - Use readable Markdown in question, options, and explanation.
    - Separate context, givens, and the actual question with real line breaks.
    - Use short paragraphs or bullet lists when they improve readability.
    - Do not add question numbers or A/B/C/D prefixes; the UI supplies them.
    - Keep options concise and consistent in wording, units, and precision.
    - Do not reveal the correct answer in the question or options.
    - Do not wrap content in code fences or pre-encode it as HTML entities.

    Mathematics:
    - Use $expression$ for inline math in questions, options, and explanations.
    - Use $$expression$$ for standalone block equations.
    - Put block delimiters on separate lines, with blank lines around the block.
    - Keep short mathematical answer options inline.
    - Preserve LaTeX braces and commands, such as $Q_{in}$ and $\frac{W}{Q_{in}}$.
    - Escape backslashes correctly when producing JSON; the parsed strings
      must contain the intended LaTeX commands.

    Explanations:
    - Explain the governing concept and why the correct option follows.
    - For calculations, show the formula, substitution, and result with units.
    - Briefly address the main misconception represented by the distractors.
    - Keep explanations focused and avoid repeating the question verbatim.
    """
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

"""Schemas for multiple-choice questions."""

from pydantic import BaseModel, Field

from .common import NonEmptyText


class MultipleChoiceQuestion(BaseModel):
    """A question with four options and one correct answer."""

    question: NonEmptyText
    options: list[NonEmptyText] = Field(min_length=4, max_length=4)
    correct_answer_index: int = Field(
        ge=0,
        le=3,
        description="Zero-based index of the correct option.",
    )
    explanation: NonEmptyText


class MultipleChoiceQuestionSet(BaseModel):
    """A quiz containing related multiple-choice questions."""

    quiz_title: NonEmptyText = Field(
        description=(
            "A concise, descriptive title identifying the quiz's main topic. "
            "For example: 'Second-Order ODEs and Phase Plane Analysis'."
        ),
    )
    description: NonEmptyText = Field(
        description=(
            "One or two sentences describing the concepts and skills assessed "
            "by the quiz. Do not include answers or repeat the title."
        ),
    )
    questions: list[MultipleChoiceQuestion] = Field(
        min_length=1,
        description="The multiple-choice questions included in this quiz.",
    )

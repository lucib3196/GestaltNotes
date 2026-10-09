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
    """A collection of multiple-choice questions."""

    questions: list[MultipleChoiceQuestion] = Field(min_length=1)

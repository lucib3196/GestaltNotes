"""Shared Pydantic models for Gestalt learning content."""

from .flashcards import Flashcard, FlashcardSet
from .multiple_choice import MultipleChoiceQuestion, MultipleChoiceQuestionSet

__all__ = [
    "Flashcard",
    "FlashcardSet",
    "MultipleChoiceQuestion",
    "MultipleChoiceQuestionSet",
]


def main() -> None:
    print("Hello from gestalt-models!")

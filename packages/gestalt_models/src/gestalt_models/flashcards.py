"""Schemas for flashcards."""

from pydantic import BaseModel, Field

from .common import NonEmptyText


class Flashcard(BaseModel):
    """A prompt on the front and its answer on the back."""

    front: NonEmptyText
    back: NonEmptyText


class FlashcardSet(BaseModel):
    """A collection of flashcards."""

    cards: list[Flashcard] = Field(min_length=1)

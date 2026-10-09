"""Package generated flashcards using shared models."""

from typing import Annotated, Literal

from gestalt_models import Flashcard, FlashcardSet
from langchain.tools import tool
from pydantic import BaseModel, Field


class FlashcardArtifact(BaseModel):
    """Wrap flashcard data for application rendering."""

    kind: Literal["flashcards"] = "flashcards"
    schema_version: Literal[2] = 2
    data: FlashcardSet


@tool(return_direct=True, response_format="content_and_artifact")
def create_flashcards(
    num_flashcards: Annotated[
        int, Field(ge=1, description="Number of flashcards requested by the user.")
    ],
    cards: list[Flashcard],
) -> tuple[str, dict]:
    """Package exactly the requested number of flashcards."""
    result = FlashcardSet(cards=cards)
    if len(result.cards) != num_flashcards:
        raise ValueError(f"Expected exactly {num_flashcards} flashcards.")
    artifact = FlashcardArtifact(data=result)
    return (
        f"Created {len(result.cards)} flashcards. Feel free to try them out!",
        artifact.model_dump(mode="json"),
    )

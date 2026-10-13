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
    r"""Package exactly the requested number of flashcards.

    Keep each front focused on one question and each back on its answer.
    These math formatting rules apply to both sides:
    - Use $expression$ for inline math within sentences.
    - Use $$expression$$ for standalone block equations.
    - Put block delimiters on separate lines, with blank lines around the block.
    - Preserve LaTeX braces and commands, such as $Q_{in}$ and $\Delta T$.
    - Escape backslashes correctly when producing JSON; the parsed strings
      must contain the intended LaTeX commands.
    """
    result = FlashcardSet(cards=cards)
    if len(result.cards) != num_flashcards:
        raise ValueError(f"Expected exactly {num_flashcards} flashcards.")
    artifact = FlashcardArtifact(data=result)
    return (
        f"Created {len(result.cards)} flashcards. Feel free to try them out!",
        artifact.model_dump(mode="json"),
    )

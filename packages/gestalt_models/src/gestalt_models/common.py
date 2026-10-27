"""Shared field types for generated learning content."""

from typing import Annotated

from pydantic import Field

NonEmptyText = Annotated[str, Field(min_length=1)]

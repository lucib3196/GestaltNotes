from typing import Literal

from pydantic import BaseModel, Field


class PaginationOptions(BaseModel):
    offset: int = Field(default=0, ge=0)
    limit: int = Field(default=20, ge=1, le=100)
    order: Literal["desc", "asc"] = "desc"

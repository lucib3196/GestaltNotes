from pydantic import BaseModel
from pydantic import Field as PydanticField


class FileUpdate(BaseModel):
    content_type: str | None = None
    size_bytes: int | None = PydanticField(default=None, ge=0)

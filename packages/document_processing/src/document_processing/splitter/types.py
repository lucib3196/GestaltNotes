from pydantic import BaseModel
from pathlib import Path
class PageChunk(BaseModel):
    """PDF bytes and their zero-based, inclusive source page range."""

    content: bytes
    start: int
    end: int
    mime_type: str

    def save(self, destination: str | Path) -> Path:
        """Write the chunk to destination, overwriting an existing file."""
        path = Path(destination)
        path.write_bytes(self.content)
        return path
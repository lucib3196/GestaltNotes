from pydantic import BaseModel
from pathlib import Path
class PageChunk(BaseModel):
    content: bytes
    start: int
    end: int
    mime_type: str

    def save(self, destination: str | Path) -> Path:
        path = Path(destination)
        path.write_bytes(self.content)
        return path
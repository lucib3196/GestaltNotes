from pathlib import Path
from typing import Protocol


class DocumentAnnotator(Protocol):
    def annotate(self, file: str | Path) -> bytes: ...

from typing import Protocol
from pathlib import Path

class DocumentAnnotator(Protocol):
    def annotate(self, file: str|Path)->bytes:...
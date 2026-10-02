from abc import ABC, abstractmethod
from pathlib import Path


class DocumentAnnotator(ABC):
    @abstractmethod
    def annotate(self, file: str | Path) -> bytes: ...

    def annotate_and_save(self, file: str | Path, destination: str | Path) -> Path:
        path = Path(destination)
        path.write_bytes(self.annotate(file))
        return path

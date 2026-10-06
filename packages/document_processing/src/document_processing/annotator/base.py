from abc import ABC, abstractmethod
from pathlib import Path


class DocumentAnnotator(ABC):
    """Produce annotated document bytes from a source file."""

    @abstractmethod
    def annotate(self, file: str | Path) -> bytes:
        """Return annotated bytes without overwriting the source."""

    def annotate_and_save(self, file: str | Path, destination: str | Path) -> Path:
        """Write annotated bytes to destination, overwriting an existing file."""
        path = Path(destination)
        path.write_bytes(self.annotate(file))
        return path

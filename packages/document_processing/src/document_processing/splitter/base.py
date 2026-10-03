from abc import ABC, abstractmethod
from pathlib import Path

from multimethod import multimethod
from pydantic import BaseModel
from .types import PageChunk




class DocumentPageSplitter(ABC):
    """Extract zero-based, inclusive page ranges from documents."""
    @multimethod
    @abstractmethod
    def extract(self, file: str | Path, start: int, end: int) -> PageChunk:
        """Extract an inclusive page range from a source file."""

    @multimethod
    @abstractmethod
    def extract(self, data: bytes, start: int, end: int) -> PageChunk:
        """Extract an inclusive page range from document bytes."""

    @multimethod
    def split(
        self, data: bytes, ranges: list[tuple[int, int]]
    ) -> list[PageChunk]:
        """Extract ranges from bytes in the supplied order."""
        return [self.extract(data, start, end) for start, end in ranges]

    @multimethod
    def split(
        self, file: str | Path, ranges: list[tuple[int, int]]
    ) -> list[PageChunk]:
        """Read a source file and extract ranges in the supplied order."""
        return self.split(Path(file).read_bytes(), ranges)

    def extract_and_save(
        self,
        source: str | Path | bytes,
        start: int,
        end: int,
        destination: str | Path,
    ) -> Path:
        """Extract a range and write it to destination, overwriting that file."""
        return self.extract(source, start, end).save(destination)

    def split_and_save(
        self,
        source: str | Path | bytes,
        ranges: list[tuple[int, int]],
        directory: str | Path,
        *,
        prefix: str = "chunk",
        suffix: str = ".pdf",
    ) -> list[Path]:
        """Save ranges as numbered chunks, overwriting matching filenames."""
        chunks = self.split(source, ranges)
        output_dir = Path(directory)
        output_dir.mkdir(parents=True, exist_ok=True)

        return [
            chunk.save(
                output_dir
                / f"{prefix}_{index}_{chunk.start}-{chunk.end}{suffix}"
            )
            for index, chunk in enumerate(chunks)
        ]

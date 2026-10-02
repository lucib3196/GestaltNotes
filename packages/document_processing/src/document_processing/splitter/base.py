from abc import ABC, abstractmethod
from pathlib import Path

from multimethod import multimethod
from pydantic import BaseModel
from .types import PageChunk




class DocumentPageSplitter(ABC):
    @multimethod
    @abstractmethod
    def extract(self, file: str | Path, start: int, end: int) -> PageChunk: ...

    @multimethod
    @abstractmethod
    def extract(self, data: bytes, start: int, end: int) -> PageChunk: ...

    @multimethod
    def split(
        self, data: bytes, ranges: list[tuple[int, int]]
    ) -> list[PageChunk]:
        return [self.extract(data, start, end) for start, end in ranges]

    @multimethod
    def split(
        self, file: str | Path, ranges: list[tuple[int, int]]
    ) -> list[PageChunk]:
        return self.split(Path(file).read_bytes(), ranges)

    def extract_and_save(
        self,
        source: str | Path | bytes,
        start: int,
        end: int,
        destination: str | Path,
    ) -> Path:
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
        chunks = self.split(source, ranges)
        output_dir = Path(directory)
        output_dir.mkdir(parents=True, exist_ok=True)

        return [
            chunk.save(
                output_dir
                / f"{prefix}_{index}_{chunk.start}-{chunk.end}{suffix}"
            )
            for index, chunk in enumerate(chunks, start=1)
        ]

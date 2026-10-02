from abc import ABC, abstractmethod
from collections.abc import Sequence
from pathlib import Path


class Converter(ABC):
    """Convert a document into binary outputs."""

    @property
    @abstractmethod
    def extension(self) -> str:
        """File extension for converted outputs."""

    @abstractmethod
    def convert(self, file: str | Path) -> Sequence[bytes]:
        """Return converted content in document order."""

    def save(
        self,
        content: Sequence[bytes],
        directory: str | Path,
        *,
        prefix: str = "page",
    ) -> list[Path]:
        """Save content with one-based numbering; overwrite matching files."""
        if (
            not prefix
            or prefix in {".", ".."}
            or "/" in prefix
            or "\\" in prefix
        ):
            raise ValueError("prefix must be a nonempty filename component")

        output_dir = Path(directory)
        output_dir.mkdir(parents=True, exist_ok=True)
        paths = []
        for number, data in enumerate(content, start=1):
            path = output_dir / f"{prefix}_{number}.{self.extension}"
            path.write_bytes(data)
            paths.append(path)
        return paths

    def convert_and_save(
        self,
        file: str | Path,
        directory: str | Path,
        *,
        prefix: str = "page",
    ) -> list[Path]:
        """Convert and save every output, returning its path."""
        return self.save(self.convert(file), directory, prefix=prefix)

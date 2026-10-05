from pathlib import Path

import pymupdf
from multimethod import multimethod
from pymupdf import Document

from .base import DocumentPageSplitter
from .types import PageChunk


class PDFPageSplitter(DocumentPageSplitter):
    """Extract PDF pages while preserving their original content."""
    def __init__(
        self,
    ) -> None:
        """Create a PDF page splitter."""
        return None

    @multimethod
    def extract(self, file: str | Path, start: int, end: int) -> PageChunk:
        """Extract a zero-based, inclusive page range from a PDF file."""
        return self._extract(file, start, end)

    @multimethod
    def extract(self, data: bytes, start: int, end: int) -> PageChunk:  # noqa: F811
        """Extract a zero-based, inclusive page range from PDF bytes."""
        return self._extract(data, start, end)

    def _extract(self, source: str | Path | bytes, start: int, end: int) -> PageChunk:
        """Validate a PDF and copy the requested pages into a new PDF."""
        with self._open_pdf(source) as doc:
            if not doc.is_pdf:
                raise ValueError("Expected a PDF document")
            if doc.needs_pass:
                raise ValueError("Password-protected PDFs are unsupported")

            self.validate_page_range(doc, start, end)

            with pymupdf.open() as dest:
                dest.insert_pdf(doc, from_page=start, to_page=end)
                return PageChunk(
                    content=dest.tobytes(),
                    start=start,
                    end=end,
                    mime_type="application/pdf",
                )

    @staticmethod
    def validate_page_range(
        document: Document,
        start_page: int,
        end_page: int,
    ) -> None:
        """Validate a 0-based, inclusive page range."""
        if type(start_page) is not int or type(end_page) is not int:
            raise TypeError("Page numbers must be integers.")

        if not 0 <= start_page <= end_page < document.page_count:
            raise ValueError(
                f"Invalid page range {start_page}-{end_page}. "
                f"Expected 0 <= start <= end < {document.page_count}."
            )

    def _open_pdf(self, source: bytes | str | Path) -> Document:
        """Open a PDF file or bytes; wrap opening failures in RuntimeError."""
        try:
            if isinstance(source, bytes):
                return pymupdf.open(stream=source, filetype="pdf")

            return pymupdf.open(filename=str(source))
        except (OSError, RuntimeError) as exc:
            raise RuntimeError(f"Could not open PDF {exc!s}") from exc



if __name__ == "__main__":
    file = r""
    PDFPageSplitter().extract_and_save(source=file, start=0, end=1, destination="./output.pdf")
from pathlib import Path
from typing import Literal

import pymupdf
from pydantic import BaseModel, ConfigDict, Field

from .base import Converter


class Config(BaseModel):
    """Configure image format and rendering scale."""

    model_config = ConfigDict(validate_assignment=True)

    extension: Literal["png", "jpg", "jpeg"] = "png"
    zoom: float = Field(default=2.0, gt=0, allow_inf_nan=False)


class PDF2ImageConverter(Converter):
    """Render each PDF page into image bytes."""

    def __init__(self, config: Config | None = None) -> None:
        """Use the supplied image format and scale, or their defaults."""
        self._config = config if config is not None else Config()

    @property
    def extension(self) -> str:
        """Return the file extension used for rendered images."""
        return self._config.extension

    def convert(self, file: str | Path | bytes) -> list[bytes]:
        """Render all pages while preserving their order and rotation."""
        description = "in-memory PDF" if isinstance(file, bytes) else str(file)
        try:
            doc = (
                pymupdf.open(stream=file, filetype="pdf")
                if isinstance(file, bytes)
                else pymupdf.open(filename=str(file))
            )
        except (OSError, RuntimeError) as exc:
            raise RuntimeError(f"Could not open PDF {description}.") from exc

        with doc:
            if not doc.is_pdf:
                raise ValueError(f"Expected a PDF document: {description}")
            if doc.needs_pass:
                raise ValueError(
                    f"Password-protected PDFs are unsupported: {description}"
                )

            matrix = pymupdf.Matrix(self._config.zoom, self._config.zoom)
            images = []
            for page in doc:
                try:
                    pixmap = page.get_pixmap(
                        matrix=matrix,
                        colorspace=pymupdf.csRGB,
                        alpha=False,
                    )
                    images.append(pixmap.tobytes(self.extension))
                except (ValueError, RuntimeError) as exc:
                    raise RuntimeError(
                        f"Could not render page index {page.number} in {description}."
                    ) from exc
            return images

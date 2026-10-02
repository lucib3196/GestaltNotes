from enum import StrEnum
from pathlib import Path

import pymupdf
from pydantic import BaseModel, ConfigDict, Field
from pymupdf import Page

from .base import DocumentAnnotator


class Anchor(StrEnum):
    """Supported corners for positioning page labels."""

    TOP_LEFT = "top-left"
    TOP_RIGHT = "top-right"
    BOTTOM_RIGHT = "bottom-right"
    BOTTOM_LEFT = "bottom-left"


class Config(BaseModel):
    """Configure label placement and size.

    Offsets are measured in PDF points, moving inward from the anchor.
    ``margin_frac`` controls both placement and circle radius.
    ``zoom`` is reserved for rendering and currently has no effect.
    """

    model_config = ConfigDict(validate_assignment=True)

    anchor: Anchor = Anchor.BOTTOM_RIGHT
    margin_frac: float = Field(default=0.1, gt=0, lt=0.5, allow_inf_nan=False)
    offset: tuple[int, int] = (20, 20)
    zoom: float = Field(default=2.0, gt=0, allow_inf_nan=False)


class PDFAnnotator(DocumentAnnotator):
    """Draw circular page-index labels and return the modified PDF."""

    def __init__(self, config: Config | None = None) -> None:
        """Use the supplied configuration or create default settings."""
        self.config = config if config is not None else Config()

    @property
    def anchor(self) -> Anchor:
        """Return the corner used to position labels."""
        return self.config.anchor

    @property
    def margin_frac(self) -> float:
        """Return the fraction used for placement and circle radius."""
        return self.config.margin_frac

    @property
    def offset(self) -> tuple[int, int]:
        """Return the horizontal and vertical offsets in PDF points."""
        return self.config.offset

    @property
    def zoom(self) -> float:
        """Return the zoom setting, currently unused by annotation."""
        return self.config.zoom

    def annotate(self, file: str | Path) -> bytes:
        """Annotate every page and return PDF bytes.

        The source file is not overwritten.

        Raises:
            ValueError: If the document is not a PDF or needs a password.
            RuntimeError: If opening, annotation, or serialization fails.
        """
        try:
            doc = pymupdf.open(file)
        except (OSError, RuntimeError) as exc:
            raise RuntimeError(f"Could not open PDF {file!s}.") from exc

        with doc:
            if not doc.is_pdf:
                raise ValueError(f"Expected a PDF document: {file!s}")
            if doc.needs_pass:
                raise ValueError(f"Password-protected PDFs are unsupported: {file!s}")

            for page in doc:
                try:
                    self.annotate_page(page)
                except (ValueError, RuntimeError) as exc:
                    raise RuntimeError(
                        f"Could not annotate page index {page.number} in {file!s}."
                    ) from exc

            try:
                return doc.tobytes()
            except (ValueError, RuntimeError) as exc:
                raise RuntimeError(
                    f"Could not serialize annotated PDF {file!s}."
                ) from exc

    def annotate_page(self, page: Page) -> None:
        """Draw a circle containing the page's zero-based index.

        Mutates the page and resets its rotation to zero.
        A failure can leave the page partially modified.

        Raises:
            ValueError: If the label falls outside the page or cannot fit.
        """
        if page.rotation != 0:
            page.set_rotation(0)

        rect = page.rect
        cx, cy = self.get_annotation_coords(
            (rect.width, rect.height),
            self.margin_frac,
            self.offset,
            self.anchor,
        )

        radius = rect.width * self.margin_frac
        label_rect = pymupdf.Rect(
            cx - radius,
            cy - radius,
            cx + radius,
            cy + radius,
        )

        # if not rect.contains(label_rect):
        #     raise ValueError(
        #         "The label extends outside the page; "
        #         "adjust margin_frac or offset."
        #     )

        # Use one shape so a text-fit failure does not commit the circle.
        shape = page.new_shape()
        shape.draw_circle(center=(cx, cy), radius=radius)
        shape.finish()

        remaining_space = shape.insert_textbox(
            label_rect,
            str(page.number),
            fontsize=radius,
            align=pymupdf.TEXT_ALIGN_CENTER,
        )
        if remaining_space < 0:
            raise ValueError("The page index does not fit inside its label.")

        shape.commit()

    @staticmethod
    def get_annotation_coords(
        size: tuple[float, float],
        margin_frac: float,
        offset: tuple[int, int],
        anchor: Anchor,
    ) -> tuple[float, float]:
        """Return a label center relative to an unrotated page.

        Positive offsets move the center inward from the selected corner.

        Raises:
            ValueError: If the anchor is unsupported.
        """
        width, height = size
        x_off, y_off = offset
        left = width * margin_frac + x_off
        top = height * margin_frac + y_off

        match anchor:
            case Anchor.TOP_LEFT:
                return left, top
            case Anchor.TOP_RIGHT:
                return width - left, top
            case Anchor.BOTTOM_LEFT:
                return left, height - top
            case Anchor.BOTTOM_RIGHT:
                return width - left, height - top
            case _:
                raise ValueError(f"Invalid anchor: {anchor!r}")


if __name__ == "__main__":
    from io import BytesIO

    import matplotlib.pyplot as plt

    file = Path(r"assets/Lec16_post.pdf").resolve()
    print(file)
    print(file.exists())
    annotator = PDFAnnotator()
    pdf_bytes = annotator.annotate(file)

    with pymupdf.open(stream=pdf_bytes, filetype="pdf") as document:
        pixmap = document[0].get_pixmap(dpi=150)
        image = plt.imread(BytesIO(pixmap.tobytes("png")), format="png")

    plt.imshow(image)
    plt.axis("off")
    plt.show()

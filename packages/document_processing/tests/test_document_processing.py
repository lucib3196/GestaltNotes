import pymupdf
import pytest
from pydantic import ValidationError

from document_processing.annotator.pdf_annotator import Anchor, Config, PDFAnnotator
from document_processing.splitter.pdf_splitter import PDFPageSplitter
from document_processing.splitter.types import PageChunk


@pytest.fixture
def pdf_source(tmp_path):
    path = tmp_path / "source.pdf"
    with pymupdf.open() as doc:
        for number in range(1, 4):
            page = doc.new_page(width=600, height=800)
            page.insert_text((72, 72), f"Page {number}")
            page.set_rotation(90)
        data = doc.tobytes()
    path.write_bytes(data)
    return path, data


@pytest.fixture
def splitter():
    return PDFPageSplitter()


@pytest.fixture(params=["bytes", "path", "str"])
def source(request, pdf_source):
    path, data = pdf_source
    return {"bytes": data, "path": path, "str": str(path)}[request.param]


def read_pages(data):
    with pymupdf.open(stream=data, filetype="pdf") as doc:
        return [(page.get_text().strip(), page.rotation) for page in doc]


@pytest.mark.parametrize("start,end", [(0, 0), (2, 2), (0, 2)])
def test_extract(splitter, source, start, end):
    chunk = splitter.extract(source, start, end)
    assert (chunk.start, chunk.end) == (start, end)
    assert chunk.mime_type == "application/pdf"
    assert read_pages(chunk.content) == [
        (f"Page {number}", 90) for number in range(start + 1, end + 2)
    ]


@pytest.mark.parametrize("start,end", [(-2, 1), (-1, 1), (2, 1), (0, 3), (3, 3)])
def test_invalid_page_ranges(splitter, pdf_source, start, end):
    _, data = pdf_source
    with pymupdf.open(stream=data, filetype="pdf") as doc:
        with pytest.raises(ValueError):
            splitter.validate_page_range(doc, start, end)


@pytest.mark.parametrize("start,end", [(True, 2), (1.0, 2), (1, "2")])
def test_page_numbers_must_be_integers(splitter, pdf_source, start, end):
    _, data = pdf_source
    with pymupdf.open(stream=data, filetype="pdf") as doc, pytest.raises(TypeError):
        splitter.validate_page_range(doc, start, end)


def test_split_preserves_requested_order(splitter, source):
    chunks = splitter.split(source, [(2, 2), (0, 1)])
    assert [read_pages(chunk.content) for chunk in chunks] == [
        [("Page 3", 90)],
        [("Page 1", 90), ("Page 2", 90)],
    ]


def test_split_empty_ranges(splitter, source):
    assert splitter.split(source, []) == []


def test_page_chunk_save(tmp_path):
    chunk = PageChunk(content=b"example", start=0, end=0, mime_type="application/pdf")
    destination = tmp_path / "chunk.pdf"
    assert chunk.save(destination) == destination
    assert destination.read_bytes() == b"example"


def test_extract_and_save(splitter, source, tmp_path):
    destination = tmp_path / "extract.pdf"
    assert splitter.extract_and_save(source, 1, 2, destination) == destination
    assert read_pages(destination.read_bytes()) == [("Page 2", 90), ("Page 3", 90)]


def test_split_and_save(splitter, source, tmp_path):
    directory = tmp_path / "nested" / "output"
    paths = splitter.split_and_save(
        source, [(0, 0), (1, 2)], directory, prefix="part", suffix=".pdf"
    )
    assert paths == [directory / "part_0_0-0.pdf", directory / "part_1_1-2.pdf"]
    assert [read_pages(path.read_bytes()) for path in paths] == [
        [("Page 1", 90)],
        [("Page 2", 90), ("Page 3", 90)],
    ]


@pytest.mark.parametrize("as_string", [False, True])
def test_annotate_preserves_source_and_adds_labels(pdf_source, as_string):
    path, original = pdf_source
    source = str(path) if as_string else path
    result = PDFAnnotator().annotate(source)
    pages = read_pages(result)
    assert len(pages) == 3
    for index, (text, rotation) in enumerate(pages):
        assert f"Page {index + 1}" in text
        assert str(index) in text.splitlines()
        assert rotation == 0
    with pymupdf.open(stream=result, filetype="pdf") as doc:
        assert all(page.get_drawings() for page in doc)
    assert path.read_bytes() == original


def test_annotate_and_save(pdf_source, tmp_path):
    source, original = pdf_source
    destination = tmp_path / "annotated.pdf"
    assert PDFAnnotator().annotate_and_save(source, destination) == destination
    assert len(read_pages(destination.read_bytes())) == 3
    assert source.read_bytes() == original


@pytest.mark.parametrize(
    "anchor,expected",
    [
        (Anchor.TOP_LEFT, (50, 60)),
        (Anchor.TOP_RIGHT, (550, 60)),
        (Anchor.BOTTOM_LEFT, (50, 740)),
        (Anchor.BOTTOM_RIGHT, (550, 740)),
    ],
)
def test_anchor_coordinates(anchor, expected):
    assert (
        PDFAnnotator.get_annotation_coords((600, 800), 0.05, (20, 20), anchor)
        == expected
    )


def test_unsupported_anchor():
    with pytest.raises(ValueError):
        PDFAnnotator.get_annotation_coords((600, 800), 0.05, (20, 20), "unsupported")


@pytest.mark.parametrize(
    "field,value",
    [
        ("margin_frac", 0),
        ("margin_frac", -0.1),
        ("margin_frac", 0.5),
        ("margin_frac", float("nan")),
        ("margin_frac", float("inf")),
        ("zoom", 0),
        ("zoom", -1),
        ("zoom", float("nan")),
        ("zoom", float("inf")),
        ("anchor", "unsupported"),
    ],
)
def test_invalid_config(field, value):
    with pytest.raises(ValidationError):
        Config(**{field: value})


def test_config_validates_assignment():
    config = Config()
    with pytest.raises(ValidationError):
        config.margin_frac = 0


@pytest.mark.parametrize("file_kind", ["missing", "corrupt"])
def test_invalid_files(splitter, tmp_path, file_kind):
    source = tmp_path / "input.pdf"
    if file_kind == "corrupt":
        source.write_bytes(b"not a PDF")
    with pytest.raises(RuntimeError):
        splitter.extract(source, 0, 0)
    with pytest.raises(RuntimeError):
        PDFAnnotator().annotate(source)


def test_password_protected_pdf(splitter, pdf_source, tmp_path):
    _, data = pdf_source
    encrypted = tmp_path / "encrypted.pdf"
    with pymupdf.open(stream=data, filetype="pdf") as doc:
        doc.save(
            encrypted,
            encryption=pymupdf.PDF_ENCRYPT_AES_256,
            owner_pw="owner-password",
            user_pw="user-password",
        )
    with pytest.raises(ValueError):
        splitter.extract(encrypted, 0, 0)
    with pytest.raises(ValueError):
        PDFAnnotator().annotate(encrypted)

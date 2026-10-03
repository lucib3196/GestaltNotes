# Semantic splitter

Split a PDF into semantic sections with a multimodal chat model.

The pipeline annotates pages with zero-based index labels, renders the annotated
PDF bytes as images, analyzes the images, and extracts sections from the original
PDF. Returned PDFs preserve the original content and rotation. All page ranges
are zero-based and inclusive. Saved page and chunk filenames also start at zero.

## Usage

```python
from langchain.chat_models import init_chat_model
from semantic_splitter.pdf_section_parser import PDFSectionParser

model = init_chat_model(model_provider="google_genai", model="gemini-2.5-flash")
sections = PDFSectionParser(model=model).parse("document.pdf")
```

Pass `structured_output=YourPydanticModel` to describe each section's metadata.
For typed results use `PDFSectionParser[YourPydanticModel]`. Without a schema,
metadata consists of string titles. `prompt` controls the section identification
instructions. The annotator, converter, and splitter can be supplied explicitly.

## Example and tests

From this package directory:

```bash
uv sync --group dev
uv run python -m semantic_splitter.pdf_section_parser
uv run pytest
```

The executable example reads the bundled three-page `assets/example.pdf` and
writes `output.json`, encoding each section's PDF bytes as base64. It loads
`.env` only when run as an example and requires Google model credentials.

The tests use that same PDF with a deterministic model response and real PDF
annotation, rendering, and splitting; they need no API key or network access.

## Package layout

- `pdf_section_parser.py`: pipeline orchestration and executable example.
- `models.py`: page ranges, images, model responses, and extracted PDF sections.
- `context.py`: model, metadata schema, and shared default prompt.
- `state.py`: graph input and processing state.
- `nodes.py`: multimodal section analysis.
- `assets/example.pdf`: shared example and test document.
- `tests/`: pipeline and converter tests.

Existing names such as `structured_output`, `PageContent`, and
`ExtractionResult.pages` remain compatible. The latter two represent section
content and section ranges, rather than individual page results.

## Async usage

```python
parser = PDFSectionParser(model=model)
sections = await parser.aparse("document.pdf")
```

`aparse` awaits the model and moves PDF annotation, rendering, and extraction
into worker threads. Both parser methods use the same compiled graph and range
validation. For direct graph execution use `parser.graph.ainvoke(input_state,
context=parser.context)` (or `invoke` for synchronous execution).

## GitHub Actions and Gemini credentials

Semantic Splitter CI runs deterministic tests on pushes and pull requests,
including changes to its document-processing and multimodal dependencies.
Ordinary tests require no secrets. Live tests are excluded by default.

Set either repository Actions secret `GOOGLE_API_KEY` or `GEMINI_API_KEY`.
Google's provider checks `GOOGLE_API_KEY` first if both are supplied. No other
credentials are required for this Gemini API workflow.

To run live tests, manually dispatch **Semantic Splitter CI** with `run_gemini`
enabled. That job exposes secrets only to the test step and exercises both
sync and async parsing. Locally, set either environment variable and run:

```bash
uv run --locked pytest -q -m integration
```

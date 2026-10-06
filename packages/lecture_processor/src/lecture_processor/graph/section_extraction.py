import base64
from importlib.resources import files

from document_processing.converter import PDF2ImageConverter
from langgraph.runtime import Runtime
from multimodal_llm import MultiModalLLM
from pydantic import BaseModel
from semantic_splitter import PDFSectionParser
from semantic_splitter.graph.context import DEFAULT_PROMPT
from semantic_splitter.parser import PDFSection

from lecture_processor.extract_derivations.model import Derivation
from lecture_processor.extracted_question.model import ExtractedQuestion
from lecture_processor.graph.models import ExtractedItems, SectionType

from .context import ExtractionContext
from .models import SectionMetadata
from .state import InputState, SectionResult, SectionTask
from .utils import resolve_context_prompts


def extract_sections(
    state: InputState,
    runtime: Runtime[ExtractionContext],
) -> dict[str, list[PDFSection[SectionMetadata]]]:
    """Identify sections using the configured segmentation prompt."""
    parser = PDFSectionParser[SectionMetadata](
        model=runtime.context.model,
        prompt=resolve_context_prompts(
            "segmentation", runtime, default_prompt=DEFAULT_PROMPT
        ),
        structured_output=SectionMetadata,
    )
    return {"sections": parser.parse(state.source)}


def extract_items[T: BaseModel](
    task: SectionTask,
    runtime: Runtime[ExtractionContext],
    *,
    item_model: type[T],
    kind: SectionType,
    prompt_folder: str,
) -> dict[str, list[SectionResult[T]]]:
    """Render raw or Base64-encoded PDF content and extract typed items."""
    document = task["section"].document
    pdf_bytes = document.content
    if not pdf_bytes.startswith(b"%PDF-"):
        pdf_bytes = base64.b64decode(pdf_bytes, validate=True)

    images = PDF2ImageConverter().convert(pdf_bytes)
    if not images:
        raise ValueError(f"Section {task['index']} contains no pages.")
    if len(images) != document.end - document.start + 1:
        raise ValueError("Section page count does not match its source range.")

    prompt = resolve_context_prompts(
        kind,
        runtime,
        default_prompt=(
            files("lecture_processor")
            .joinpath(prompt_folder, "prompt.txt")
            .read_text(encoding="utf-8")
        ),
    )
    page_mapping = "\n".join(
        f"Image {index + 1}: original PDF page index {document.start + index}"
        for index in range(len(images))
    )
    prompt += (
        "\n\nReturn every matching item in the items list; "
        "return [] if none are present.\n"
        "Use this mapping for all references, ignoring printed page numbers:\n"
        f"{page_mapping}"
    )
    output_model = ExtractedItems[item_model]
    response = MultiModalLLM(runtime.context.model).invoke(
        prompt=prompt,
        images=images,
        mime_type="image/png",
        output_model=output_model,
    )
    extracted = output_model.model_validate(response)
    return {
        "results": [
            SectionResult[item_model](
                index=task["index"], kind=kind, items=extracted.items
            )
        ]
    }


def extract_derivations(
    task: SectionTask,
    runtime: Runtime[ExtractionContext],
) -> dict[str, list[SectionResult[Derivation]]]:
    return extract_items(
        task,
        runtime,
        item_model=Derivation,
        kind="derivation",
        prompt_folder="extract_derivations",
    )


def extract_questions(
    task: SectionTask,
    runtime: Runtime[ExtractionContext],
) -> dict[str, list[SectionResult[ExtractedQuestion]]]:
    return extract_items(
        task,
        runtime,
        item_model=ExtractedQuestion,
        kind="question",
        prompt_folder="extracted_question",
    )


SECTION_PREPARATION_NODES = {
    "extract_sections": extract_sections,
}

SECTION_EXTRACTION_NODES = {
    "extract_derivations": extract_derivations,
    "extract_questions": extract_questions,
}

__all__ = ["SECTION_EXTRACTION_NODES", "SECTION_PREPARATION_NODES"]

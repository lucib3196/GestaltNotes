from collections.abc import Iterator
from typing import Any

from langchain_core.documents import Document

from lecture_processor.conceptual_question import ConceptualQuestion
from lecture_processor.extract_derivations.model import Derivation
from lecture_processor.extracted_question.model import ExtractedQuestion
from lecture_processor.graph.state import OutputState


def _item_to_document(
    item: ConceptualQuestion | Derivation | ExtractedQuestion,
) -> Document:
    metadata: dict[str, Any] = {}

    if isinstance(item, Derivation):
        metadata.update(
            kind="derivation",
            completeness=item.completeness,
        )
    elif isinstance(item, ExtractedQuestion):
        metadata.update(
            kind="extracted_question",
            question_type=item.kind,
        )
    elif isinstance(item, ConceptualQuestion):
        metadata["kind"] = "conceptual_question"
    else:
        raise TypeError(f"Unsupported item type: {type(item).__name__}")

    if item.reference is not None:
        # Preserve the models' zero-based, inclusive page indices.
        metadata["page_start"] = item.reference.start
        metadata["page_end"] = item.reference.end

    return Document(
        page_content=item.as_string(),
        metadata=metadata,
    )


def parse_lecture_documents(source: Any) -> Iterator[Document]:
    data = OutputState.model_validate(source)
    full_lecture = ""

    if data.lecture_summary is not None:
        full_lecture += f"\n{data.lecture_summary.as_string()}"
        yield Document(
            page_content=data.lecture_summary.as_string(),
            metadata={"kind": "lecture_summary"},
        )

    for question in data.conceptual_questions:
        full_lecture += f"\n{question.as_string()}"
        yield _item_to_document(question)

    for section in data.results:
        for item in section.items:
            full_lecture += f"\n{item.as_string()}"
            document = _item_to_document(item)
            document.metadata["section_index"] = section.index
            yield document
    yield (Document(page_content=full_lecture, metadata={"kind": "full_lecture"}))


if __name__ == "__main__":
    from pathlib import Path
    import json

    source = json.loads(Path("full_output.json").read_text())
    docs = parse_lecture_documents(source)
    full = [d for d in docs]


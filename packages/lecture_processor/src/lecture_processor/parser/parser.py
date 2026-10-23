from collections.abc import Iterator
from typing import Any, Literal

from langchain_core.documents import Document
from pydantic import BaseModel, Field
from lecture_processor.conceptual_question import ConceptualQuestion
from lecture_processor.extract_derivations.model import Derivation
from lecture_processor.extracted_question.model import ExtractedQuestion
from lecture_processor.graph.state import OutputState


class ParsedNoteBlock(BaseModel):
    title: str
    kind: Literal[
        "lecture_summary",
        "conceptual_question",
        "derivation",
        "extracted_question",
    ]
    position: int = Field(ge=0)
    section_index: int | None = None
    content: dict[str, Any]


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


def parse_lecture_note_blocks(
    source: Any,
) -> Iterator[tuple[ParsedNoteBlock, Document]]:
    """Pair editable extraction data with its searchable representation."""
    data = OutputState.model_validate(source)
    position = 0

    if data.lecture_summary is not None:
        summary = data.lecture_summary
        yield (
            ParsedNoteBlock(
                title=summary.title,
                kind="lecture_summary",
                position=position,
                content=summary.model_dump(mode="json"),
            ),
            Document(
                page_content=summary.as_string(),
                metadata={"kind": "lecture_summary"},
            ),
        )
        position += 1

    for question in data.conceptual_questions:
        yield (
            ParsedNoteBlock(
                title=question.question,
                kind="conceptual_question",
                position=position,
                content=question.model_dump(mode="json"),
            ),
            _item_to_document(question),
        )
        position += 1

    for section in sorted(data.results, key=lambda section: section.index):
        for item in section.items:
            if isinstance(item, Derivation):
                title = item.title
                kind = "derivation"
            elif isinstance(item, ExtractedQuestion):
                title = item.question
                kind = "extracted_question"
            else:
                raise TypeError(f"Unsupported item type: {type(item).__name__}")

            document = _item_to_document(item)
            document.metadata["section_index"] = section.index
            yield (
                ParsedNoteBlock(
                    title=title,
                    kind=kind,
                    position=position,
                    section_index=section.index,
                    content=item.model_dump(mode="json"),
                ),
                document,
            )
            position += 1


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
    docs = parse_lecture_note_blocks(source)
    parsed = []
    for idx, (note, doc) in enumerate(docs):
        print(f"IDX: {idx}")
        print("NOTE: ", note)
        print("DOC", doc)

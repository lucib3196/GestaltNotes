from uuid import UUID

from lecture_processor.extract_derivations.model import Derivation
from lecture_processor.extracted_question import ExtractedQuestion
from lecture_processor.graph.state import OutputState
from pydantic import BaseModel

from .models import NoteBlock


def parse_lecture_document(
    source: object,
    *,
    source_file_id: UUID | None = None,
    course_id: UUID | None = None,
) -> list[NoteBlock]:
    data = OutputState.model_validate(source)
    notes: list[NoteBlock] = []

    def append_block(
        item: BaseModel,
        *,
        title: str,
        kind: str,
        page_start: int | None = None,
        page_end: int | None = None,
    ) -> None:
        notes.append(
            NoteBlock(
                source_file_id=source_file_id,
                course_id=course_id,
                title=title,
                kind=kind,
                content=item.model_dump(mode="json"),
                position=len(notes),
                page_start=page_start,
                page_end=page_end,
            )
        )

    if data.lecture_summary is not None:
        summary = data.lecture_summary
        append_block(summary, title=summary.title, kind="lecture_summary")

    for question in data.conceptual_questions:
        reference = question.reference
        append_block(
            question,
            title=question.question,
            kind="conceptual_question",
            page_start=reference.start if reference is not None else None,
            page_end=reference.end if reference is not None else None,
        )

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

            reference = item.reference
            append_block(
                item,
                title=title,
                kind=kind,
                page_start=reference.start if reference is not None else None,
                page_end=reference.end if reference is not None else None,
            )

    return notes

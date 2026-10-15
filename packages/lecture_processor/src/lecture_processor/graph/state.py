import operator
from pathlib import Path
from typing import Annotated, Literal, TypedDict

from pydantic import BaseModel, Field
from semantic_splitter.parser import PDFSection

from lecture_processor.conceptual_question import ConceptualQuestion
from lecture_processor.extract_derivations.model import Derivation
from lecture_processor.extracted_question import ExtractedQuestion
from lecture_processor.graph.models import SectionMetadata, SectionType
from lecture_processor.lecture_analysis import LectureAnalysis


class SectionResult[T: BaseModel](BaseModel):
    index: int
    kind: SectionType
    items: list[T]


TypedSectionResult = SectionResult[Derivation] | SectionResult[ExtractedQuestion]


class InputState(BaseModel):
    source: str | Path


class State(InputState):
    lecture_images: list[bytes] = Field(default_factory=list)
    conceptual_questions: list[ConceptualQuestion] = Field(default_factory=list)
    lecture_summary: LectureAnalysis | None = None
    sections: list[PDFSection[SectionMetadata]] = Field(default_factory=list)
    results: Annotated[list[TypedSectionResult], operator.add] = Field(
        default_factory=list
    )
    failures: Annotated[list[TaskFailure], operator.add] = Field(default_factory=list)


class OutputState(InputState):
    conceptual_questions: list[ConceptualQuestion] = Field(default_factory=list)
    lecture_summary: LectureAnalysis | None = None
    sections: list[PDFSection[SectionMetadata]] = Field(default_factory=list)
    results: Annotated[list[TypedSectionResult], operator.add] = Field(
        default_factory=list
    )
    failures: Annotated[list[TaskFailure], operator.add] = Field(default_factory=list)


class SectionTask(TypedDict):
    index: int
    section: PDFSection[SectionMetadata]


class TaskFailure(BaseModel):
    task: str
    section_index: int | None = None
    kind: Literal[
        "input",
        "provider",
        "validation",
        "unexpected",
    ]
    message: str
    attempts: int | str

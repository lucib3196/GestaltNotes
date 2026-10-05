from pathlib import Path
from langgraph.runtime import Runtime
from pydantic import BaseModel
from semantic_splitter import PDFSectionParser
from typing import Literal
from lecture_processor.graph.context import ExtractionContext
from langchain.chat_models import init_chat_model
from pathlib import Path
from semantic_splitter.utils import to_serializable
from .context import ExtractionContext
from pathlib import Path
import base64
from langgraph.graph import END, START, StateGraph
from pydantic import BaseModel
from semantic_splitter.parser import PDFSection
from typing import List


class SectionMetadata(BaseModel):
    section: Literal["derivation", "question"]


class InputState(BaseModel):
    source: str | Path


class State(InputState):
    sections: List[PDFSection[SectionMetadata]]


def extract_sections(state: InputState, runtime: Runtime[ExtractionContext]):
    parser = PDFSectionParser[SectionMetadata](
        model=runtime.context.model,
        structured_output=SectionMetadata,
    )
    sections = parser.parse(state.source)
    return {"sections": sections}


builder = StateGraph(
    state_schema=State, input_schema=InputState, context_schema=ExtractionContext
)
builder.add_node("extract", extract_sections)
builder.add_edge(START, "extract")
builder.add_edge("extract", END)
graph = builder.compile()


if __name__ == "__main__":
    from pathlib import Path
    from dotenv import load_dotenv
    import json

    load_dotenv()

    file = Path(
        r"/home/lberm/projects/gestalt/GestaltNotes/packages/document_processing/src/document_processing/assets/output.pdf"
    ).resolve()
    model = init_chat_model(
        model_provider="google_genai",
        model="gemini-2.5-flash",
    )
    result = graph.invoke(
    InputState(source=file),
    context=ExtractionContext(
        model=model,
        prompt=(
            "Identify sections containing any of the following:\n"
            "- derivation: Mathematical or logical steps establishing an "
            "equation, relationship, or result.\n"
            "- question: A practice question, exercise, or worked example, "
            "with or without a solution.\n"
            "Return each section using the supplied schema. Include the full "
            "question, solution, or derivation across all relevant pages. "
            "A section may contain more than one category; preserve overlapping "
            "page ranges when needed. Exclude standalone formulas and general "
            "discussion unless they support one of these categories.\n"
            "Use zero-based, inclusive page ranges based on the supplied "
            "page-index labels, not printed page numbers. "
            "Do not invent content absent from the source."
        ),
    ),
)
    Path("./full_output.json").write_text(json.dumps(to_serializable(result)))
    

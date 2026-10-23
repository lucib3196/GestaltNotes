from typing import Literal

from langgraph.graph import END
from langgraph.runtime import Runtime
from langgraph.types import Send

from lecture_processor.graph.models import SectionType

from .context import ExtractionContext
from .state import InputState, State


def route_sections(
    state: State,
    runtime: Runtime[ExtractionContext],
) -> list[Send] | Literal["__end__"]:
    """Dispatch sections to enabled extraction tasks, or end if none qualify."""
    task_names = {
        "derivation": "derivation",
        "question": "question",
    }
    routes: dict[SectionType, str] = {
        "derivation": "extract_derivations",
        "question": "extract_questions",
    }

    sends = [
        Send(
            routes[section.metadata.section],
            {"index": index, "section": section},
        )
        for index, section in enumerate(state.sections)
        if task_names[section.metadata.section] in runtime.context.tasks
    ]
    return sends or END  # type: ignore


def route_tasks(state: InputState, runtime: Runtime[ExtractionContext]):
    """Route enabled tasks to section extraction or lecture preparation, or end."""
    tasks = runtime.context.tasks
    routes = []
    if tasks & {"derivation", "question"}:
        routes.append("extract_sections")
    if tasks & {"conceptual_questions", "summary"}:
        routes.append("prepare_lecture")
    return routes or [END]


def route_generation(state: State, runtime: Runtime[ExtractionContext]) -> list[str]:
    """Route to enabled question and summary generators, or end."""
    tasks = runtime.context.tasks
    routes = []
    if "conceptual_questions" in tasks:
        routes.append("generate_conceptual_questions")
    if "summary" in tasks:
        routes.append("generate_lecture_summary")
    return routes or [END]

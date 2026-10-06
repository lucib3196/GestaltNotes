from importlib.resources import files

from document_processing.converter import PDF2ImageConverter
from langgraph.runtime import Runtime
from multimodal_llm import MultiModalLLM
from pydantic import BaseModel, Field, create_model

from lecture_processor.conceptual_question import ConceptualQuestion
from lecture_processor.graph.models import ExtractedItems
from lecture_processor.lecture_analysis import LectureAnalysis

from .context import ExtractionContext
from .state import InputState, State
from .utils import resolve_context_prompts


def prepare_lecture(state: InputState) -> dict[str, list[bytes]]:
    """Render the full lecture once for both generation branches."""
    images = PDF2ImageConverter().convert(state.source)
    if not images:
        raise ValueError("The lecture contains no pages.")
    return {"lecture_images": images}


def generate_lecture_content[T: BaseModel](
    state: State,
    runtime: Runtime[ExtractionContext],
    *,
    output_model: type[T],
    prompt: str,
) -> T:
    """Generate structured content from the entire lecture."""
    response = MultiModalLLM(runtime.context.model).invoke(
        prompt=prompt,
        images=state.lecture_images,
        mime_type="image/png",
        output_model=output_model,
    )
    return output_model.model_validate(response)


def generate_conceptual_questions(
    state: State,
    runtime: Runtime[ExtractionContext],
) -> dict[str, list[ConceptualQuestion]]:
    num_questions = runtime.context.conceptual_questions.num_questions
    output_model = ExtractedItems[ConceptualQuestion]
    if num_questions is not None:
        output_model = create_model(
            f"ConceptualQuestionsOutput{num_questions}",
            __base__=ExtractedItems[ConceptualQuestion],
            items=(
                list[ConceptualQuestion],
                Field(min_length=num_questions, max_length=num_questions),
            ),
        )
    output = generate_lecture_content(
        state,
        runtime,
        output_model=output_model,
        prompt=resolve_context_prompts(
            "conceptual_questions",
            runtime,
            default_prompt=(
                files("lecture_processor")
                .joinpath("conceptual_question", "generation_prompt.txt")
                .read_text(encoding="utf-8")
            ),
        ),
    )
    return {"conceptual_questions": output.items}


def generate_lecture_summary(
    state: State,
    runtime: Runtime[ExtractionContext],
) -> dict[str, LectureAnalysis]:
    prompt = resolve_context_prompts(
        "summary",
        runtime,
        default_prompt=(
            files("lecture_processor")
            .joinpath("lecture_analysis", "prompt.txt")
            .read_text(encoding="utf-8")
        ),
    )
    summary = generate_lecture_content(
        state, runtime, output_model=LectureAnalysis, prompt=prompt
    )
    return {"lecture_summary": summary}


LECTURE_PREPARATION_NODES = {"prepare_lecture": prepare_lecture}

CONTENT_GENERATION_NODES = {
    "generate_conceptual_questions": generate_conceptual_questions,
    "generate_lecture_summary": generate_lecture_summary,
}


__all__ = ["CONTENT_GENERATION_NODES", "LECTURE_PREPARATION_NODES"]

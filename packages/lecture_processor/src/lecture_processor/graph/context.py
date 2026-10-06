from typing import Literal

from langchain_core.language_models import BaseChatModel
from pydantic import BaseModel, Field

TaskName = Literal["derivation", "question", "conceptual_questions", "summary"]
PromptName = Literal[
    "segmentation",
    "derivation",
    "question",
    "conceptual_questions",
    "summary",
]


class ConceptualQuestionConfig(BaseModel):
    num_questions: int = Field(default=3, gt=0, strict=True)


class FailureConfig(BaseModel):
    policy: Literal["strict", "partial"] = "partial"
    max_attempts: int = Field(default=3, ge=1)


class ExtractionContext(BaseModel):
    model: BaseChatModel
    tasks: set[TaskName] = Field(
        default_factory=lambda: {
            "derivation",
            "question",
            "conceptual_questions",
            "summary",
        }
    )
    prompts: dict[PromptName, str] = Field(default_factory=dict)
    conceptual_questions: ConceptualQuestionConfig = Field(
        default_factory=ConceptualQuestionConfig
    )
    failure: FailureConfig = Field(default_factory=FailureConfig)

from datetime import datetime
from enum import StrEnum
from typing import Annotated, Any
from uuid import UUID, uuid4

from pydantic import BaseModel, ConfigDict
from sqlalchemy import JSON, Column
from sqlalchemy.dialects.postgresql import JSONB
from sqlmodel import Field, SQLModel

JSONType = JSON().with_variant(JSONB, "postgresql")


# Database Definition


class GeneratedMCQ(SQLModel, table=True):
    id: UUID | None = Field(default_factory=uuid4, primary_key=True)

    quiz_data: dict[str, Any] = Field(
        default_factory=dict,
        sa_column=Column(JSONType, nullable=False),
    )
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

    schema_version: int = Field(default=1)

    user_id: UUID = Field(foreign_key="user.id")
    thread_id: UUID = Field(foreign_key="thread.id")


# Generated Content


class DifficultyLevel(StrEnum):
    EASY = "easy"
    MEDIUM = "medium"
    HARD = "hard"


class LearningObjective(StrEnum):
    CONCEPTUAL_UNDERSTANDING = "conceptual_understanding"
    PROBLEM_SOLVING = "problem_solving"
    EQUATION_APPLICATION = "equation_application"
    CRITICAL_THINKING = "critical_thinking"
    DEFINITION_RECALL = "definition_recall"
    MULTI_STEP_REASONING = "multi_step_reasoning"
    REAL_WORLD_APPLICATION = "real_world_application"
    DATA_INTERPRETATION = "data_interpretation"
    DESIGN_ANALYSIS = "design_analysis"


class MCQInput(BaseModel):
    topic: Annotated[
        str,
        Field(
            description=(
                "Main topic or concept the multiple choice question should "
                "focus on. Examples: 'First Law of Thermodynamics', "
                "'PID Control', 'Fluid Statics', 'Python Dictionaries'."
            )
        ),
    ]

    difficulty: Annotated[
        DifficultyLevel,
        Field(
            description=(
                "Difficulty level of the question. "
                "'easy' should test basic recall or direct application, "
                "'medium' should involve moderate reasoning or calculations, "
                "and 'hard' should involve multi-step reasoning, derivations, "
                "or conceptual depth."
            )
        ),
    ] = DifficultyLevel.MEDIUM

    num_questions: Annotated[
        int,
        Field(
            default=4,
            ge=2,
            le=6,
            description=(
                "Number of multiple-choice questions to generate. "
                "Must be between 2 and 6."
            ),
        ),
    ]

    context: Annotated[
        str,
        Field(
            description=(
                "Surrounding contextual information used to ground the question. "
                "This may include lecture notes, textbook excerpts, derivations, "
                "discussion summaries, or previously discussed concepts."
            )
        ),
    ]

    learning_objective: Annotated[
        LearningObjective,
        Field(
            description=(
                "Primary educational objective the question is intended to assess. "
                "Used internally for classification, filtering, analytics, "
                "and adaptive question generation."
            )
        ),
    ]


class Option(BaseModel):
    option: Annotated[
        str,
        Field(
            description="Answer option text shown to the learner for a given question."
        ),
    ]
    correct: Annotated[
        bool,
        Field(
            description=(
                "Whether this option is the correct answer. Exactly one option "
                "should be true per question."
            )
        ),
    ]


class MultipleChoiceQuestionBase(BaseModel):
    question: Annotated[
        str,
        Field(
            description=(
                "The complete multiple-choice question stem presented to the learner."
            )
        ),
    ]
    options: Annotated[
        list[Option],
        Field(
            description=(
                "List of answer options for the question. Should contain plausible "
                "distractors and exactly one correct option."
            )
        ),
    ]


class MultipleChoiceQuestionResponse(BaseModel):
    questions: Annotated[
        list[MultipleChoiceQuestionBase],
        Field(
            description=(
                "Generated set of multiple-choice questions matching the requested "
                "topic, context, and learning objective."
            )
        ),
    ]
    num_options: Annotated[
        int,
        Field(
            description=(
                "Number of options per question used in the generated set "
                "(typically 4)."
            )
        ),
    ]


class MultipleChoiceQuestion(MultipleChoiceQuestionBase):
    topic: Annotated[
        str,
        Field(description="Topic label attached to each generated question."),
    ]
    difficulty: Annotated[
        DifficultyLevel,
        Field(description="Difficulty label attached to each generated question."),
    ]
    learning_objective: Annotated[
        LearningObjective,
        Field(
            description=(
                "Learning objective label describing what skill the question "
                "is designed to assess."
            )
        ),
    ]


class UserSubmission(BaseModel):
    qid: int | str
    selected: str
    is_correct: bool | str


class MCQV1(MultipleChoiceQuestion):
    user_submission: UserSubmission | None = None
    model_config = ConfigDict(extra="allow")


class MCQResponseV1(BaseModel):
    payload: list[MCQV1]

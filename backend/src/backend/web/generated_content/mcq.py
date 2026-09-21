from collections.abc import Sequence
from uuid import UUID

from fastapi.exceptions import HTTPException
from fastapi.routing import APIRouter
from pydantic import BaseModel

from src.model.generated_content import MCQV1, GeneratedMCQ, MCQResponseV1
from src.service.generated_content.exceptions import (
    GeneratedContentBatchSaveError,
    GeneratedContentPersistenceError,
    GeneratedContentRetrievalError,
    GeneratedContentValidationError,
    UnsupportedSchemaVersionError,
)
from src.web.user.dependencies import CurrentUser

from .dependencies import GenMCQDependency

ID = UUID | str

router = APIRouter(
    prefix="/generated_content/mcq", tags=["users", "generated_content", "mcq"]
)


class Payload(BaseModel):
    qpayload: MCQResponseV1
    thread_id: ID


@router.post("/v1")
async def save_mcq(payload: Payload, user: CurrentUser, genmcq: GenMCQDependency):
    try:
        return await genmcq.async_batch_add_mcq(
            payload.qpayload,
            user_id=user,
            thread_id=payload.thread_id,
            schema_version=1,
        )
    except (GeneratedContentValidationError, UnsupportedSchemaVersionError) as e:
        raise HTTPException(
            detail=f"Invalid MCQ payload: {e}",
            status_code=400,
        ) from e
    except (GeneratedContentPersistenceError, GeneratedContentBatchSaveError) as e:
        raise HTTPException(
            detail=f"Failed to save generated MCQs: {e}",
            status_code=500,
        ) from e


@router.get("/v1/all")
async def get_all_questions(
    user: CurrentUser, genmcq: GenMCQDependency
) -> Sequence[GeneratedMCQ]:
    try:
        return await genmcq.retrieve_all_mcq_user(
            user_id=user,
        )
    except GeneratedContentRetrievalError as e:
        raise HTTPException(
            detail=f"Failed to retrieve generated MCQs: {e}",
            status_code=500,
        ) from e


@router.get("/v1/all/quiz")
async def get_all_quizzes(
    user: CurrentUser, genmcq: GenMCQDependency
) -> Sequence[MCQV1]:
    try:
        return await genmcq.retrive_all_mcq_user_quiz(
            user_id=user,
        )
    except (GeneratedContentValidationError, UnsupportedSchemaVersionError) as e:
        raise HTTPException(
            detail=f"Invalid stored MCQ data: {e}",
            status_code=500,
        ) from e
    except GeneratedContentRetrievalError as e:
        raise HTTPException(
            detail=f"Failed to retrieve generated quizzes: {e}",
            status_code=500,
        ) from e

from typing import Annotated
from uuid import UUID

from authorization import AccessDeniedError
from fastapi import APIRouter, HTTPException, Query, Response
from starlette import status

from backend.chat.exceptions import PromptNotFoundError, PromptServiceError
from backend.chat.model import Prompt, PromptBase, PromptSummary, PromptUpdate
from backend.chat.service.prompt_service import PromptListOptions
from backend.web.accounts.dependencies import CurrentUserDep

from .dependencies import PromptServiceDep

router = APIRouter(prefix="/prompts", tags=["prompts"])


def prompt_http_error(exc: PromptServiceError | AccessDeniedError) -> HTTPException:
    if isinstance(exc, PromptNotFoundError):
        return HTTPException(status.HTTP_404_NOT_FOUND, "Prompt not found")
    if isinstance(exc, AccessDeniedError):
        return HTTPException(status.HTTP_403_FORBIDDEN, "Access denied")
    return HTTPException(
        status.HTTP_500_INTERNAL_SERVER_ERROR, "Prompt operation failed"
    )


@router.post("/", response_model=Prompt, status_code=status.HTTP_201_CREATED)
async def create(
    service: PromptServiceDep, data: PromptBase, user: CurrentUserDep
) -> Prompt:
    try:
        return await service.create(data, user)
    except (PromptServiceError, AccessDeniedError) as exc:
        raise prompt_http_error(exc) from exc


@router.get("/", response_model=list[PromptSummary])
async def list_prompts(
    service: PromptServiceDep,
    user: CurrentUserDep,
    options: Annotated[PromptListOptions, Query()],
) -> list[PromptSummary]:
    try:
        return list(
            await service.list_user_prompts_by_title(
                user=user,
                options=options,
            )
        )
    except (PromptServiceError, AccessDeniedError) as exc:
        raise prompt_http_error(exc) from exc


@router.get("/{prompt_id}", response_model=Prompt)
async def get_prompt(
    prompt_id: UUID,
    service: PromptServiceDep,
    user: CurrentUserDep,
) -> Prompt:
    try:
        return await service.get_prompt_by_id(prompt_id, user)
    except (PromptServiceError, AccessDeniedError) as exc:
        raise prompt_http_error(exc) from exc


@router.put("/{prompt_id}", response_model=Prompt)
async def update_prompt(
    prompt_id: UUID,
    service: PromptServiceDep,
    update: PromptUpdate,
    user: CurrentUserDep,
) -> Prompt:
    try:
        return await service.update_prompt(prompt_id, update, user)
    except (PromptServiceError, AccessDeniedError) as exc:
        raise prompt_http_error(exc) from exc


@router.delete("/{prompt_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_prompt(
    prompt_id: UUID,
    service: PromptServiceDep,
    user: CurrentUserDep,
) -> Response:
    try:
        await service.delete_prompt(prompt_id, user)
    except (PromptServiceError, AccessDeniedError) as exc:
        raise prompt_http_error(exc) from exc
    return Response(status_code=status.HTTP_204_NO_CONTENT)

from typing import Any
from uuid import UUID

from fastapi import APIRouter, HTTPException

from backend.chat.exceptions import (
    ThreadBaseException,
    ThreadClientDeleteError,
    ThreadDeleteCommitError,
    ThreadDeleteError,
    ThreadMessageRetrievalError,
    ThreadNotFound,
)
from backend.chat.model import Message, Thread
from backend.chat.schema import MessageCreate, ThreadCreate, ThreadUpdate
from backend.web.accounts.dependencies import CurrentUser
from backend.web.dependencies import MessageDBDependency

from .dependencies import ThreadServiceDependency

router = APIRouter(prefix="/threads", tags=["threads"])


def thread_http_error(exc: ThreadBaseException) -> HTTPException:
    if isinstance(exc, ThreadNotFound):
        return HTTPException(404, "Thread not found")
    if isinstance(exc, ThreadMessageRetrievalError):
        return HTTPException(502, "Failed to retrieve messages")
    if isinstance(exc, ThreadClientDeleteError):
        return HTTPException(502, "Failed to delete remote thread")
    if isinstance(exc, ThreadDeleteCommitError):
        return HTTPException(500, "Remote thread deleted, but local deletion failed")
    if isinstance(exc, ThreadDeleteError):
        return HTTPException(500, "Failed to delete thread")
    return HTTPException(500, "Thread operation failed")


@router.post("/", response_model=Thread)
async def create_thread(
    data: ThreadCreate,
    service: ThreadServiceDependency,
    user: CurrentUser,
) -> Thread:
    try:
        return await service.create_thread(
            thread_id=data.thread_id,
            user_id=user,
            title=data.title,
            agent=data.agent,
        )
    except ThreadBaseException as exc:
        raise thread_http_error(exc) from exc


@router.get("/", response_model=list[Thread])
async def list_my_threads(
    service: ThreadServiceDependency,
    user: CurrentUser,
) -> list[Thread]:
    try:
        return await service.list_threads_for_user(user_id=user)
    except ThreadBaseException as exc:
        raise thread_http_error(exc) from exc


@router.post("/{thread_id}/messages", response_model=Message)
async def create_message(
    thread_id: UUID,
    data: MessageCreate,
    mdb: MessageDBDependency,
    service: ThreadServiceDependency,
    user: CurrentUser,
) -> Message:
    try:
        await service.assert_thread_owner(user, thread_id)
        msg = await mdb.create_message(
            thread_id=thread_id,
            role=data.role,
            content=data.content,
        )
        await service.touch_updated_at(user, thread_id)
        return msg
    except ThreadBaseException as exc:
        raise thread_http_error(exc) from exc
    except Exception as exc:
        raise HTTPException(500, "Failed to create message") from exc


@router.get("/{thread_id}/messages", response_model=list[dict[str, Any]])
async def get_messages(
    thread_id: UUID,
    service: ThreadServiceDependency,
    user: CurrentUser,
) -> list[dict[str, Any]]:
    try:
        return await service.get_messages(user, thread_id)
    except ThreadBaseException as exc:
        raise thread_http_error(exc) from exc


@router.get("/{thread_id}", response_model=Thread)
async def get_thread(
    thread_id: UUID, service: ThreadServiceDependency, user: CurrentUser
) -> Thread:
    try:
        return await service.get_thread_for_user(user, thread_id)
    except ThreadBaseException as exc:
        raise thread_http_error(exc) from exc


@router.put("/{thread_id}", response_model=Thread)
async def update_thread(
    thread_id: UUID,
    service: ThreadServiceDependency,
    thread_update: ThreadUpdate,
    user: CurrentUser,
) -> Thread:
    try:
        return await service.update_thread(user, thread_id, thread_update)
    except ThreadBaseException as exc:
        raise thread_http_error(exc) from exc


@router.delete("/{thread_id}", status_code=204)
async def delete_thread(
    thread_id: UUID,
    service: ThreadServiceDependency,
    user: CurrentUser,
) -> None:
    try:
        await service.delete_thread(user, thread_id)
    except ThreadBaseException as exc:
        raise thread_http_error(exc) from exc

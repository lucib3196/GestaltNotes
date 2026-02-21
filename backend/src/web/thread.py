from fastapi.routing import APIRouter
from uuid import UUID

from .dependencies import ThreadDBDependency, MessageDBDependency
from src.model.chat import Thread, Message

router = APIRouter(prefix="/threads", tags=["threads"])


@router.post("/")
async def create_thread(
    tdb: ThreadDBDependency,
    user_id: UUID,
    course_id: UUID,
    title: str | None = None,
    agent: str | None = None,
) -> Thread:
    return await tdb.create_thread(user_id=user_id, course_id=course_id, title=title, agent=agent)


@router.get("/")
async def list_threads(
    tdb: ThreadDBDependency,
    user_id: UUID,
    course_id: UUID | None = None,
) -> list[Thread]:
    return await tdb.list_threads_for_user(user_id=user_id, course_id=course_id)


@router.get("/{thread_id}")
async def get_thread(tdb: ThreadDBDependency, thread_id: UUID) -> Thread:
    return await tdb.get_thread(thread_id)


@router.post("/{thread_id}/messages")
async def create_message(
    mdb: MessageDBDependency,
    tdb: ThreadDBDependency,
    thread_id: UUID,
    role: str,
    content: str,
) -> Message:
    msg = await mdb.create_message(thread_id=thread_id, role=role, content=content)
    await tdb.touch_updated_at(thread_id)
    return msg


@router.get("/{thread_id}/messages")
async def list_messages(mdb: MessageDBDependency, thread_id: UUID) -> list[Message]:
    return await mdb.list_messages(thread_id)
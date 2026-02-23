from fastapi.routing import APIRouter
from uuid import UUID

from .dependencies import ThreadDBDependency, MessageDBDependency
from src.model.chat import Thread, Message
from .thread_model import ThreadCreate, ThreadList, MessageCreate

router = APIRouter(prefix="/threads", tags=["threads"])

@router.post("/", response_model=Thread)
async def create_thread(
    data: ThreadCreate,
    tdb: ThreadDBDependency,
) -> Thread:
    return await tdb.create_thread(
        user_id=data.user_id,
        course_id=data.course_id,
        title=data.title,
        agent=data.agent,
    )


@router.get("/", response_model=list[Thread])
async def list_threads(
    data: ThreadList,
    tdb: ThreadDBDependency,
) -> list[Thread]:
    return await tdb.list_threads_for_user(
        user_id=data.user_id,
        course_id=data.course_id,
    )


@router.get("/{thread_id}", response_model=Thread)
async def get_thread(
    thread_id: UUID,
    tdb: ThreadDBDependency,
) -> Thread:
    return await tdb.get_thread(thread_id)


@router.post("/{thread_id}/messages", response_model=Message)
async def create_message(
    thread_id: UUID,
    data: MessageCreate,
    mdb: MessageDBDependency,
    tdb: ThreadDBDependency,
) -> Message:
    msg = await mdb.create_message(
        thread_id=thread_id,
        role=data.role,
        content=data.content,
    )
    await tdb.touch_updated_at(thread_id)
    return msg


@router.get("/{thread_id}/messages", response_model=list[Message])
async def list_messages(
    thread_id: UUID,
    mdb: MessageDBDependency,
) -> list[Message]:
    return await mdb.list_messages(thread_id)
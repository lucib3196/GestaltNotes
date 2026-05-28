from uuid import UUID

from fastapi.exceptions import HTTPException
from fastapi.routing import APIRouter
from starlette import status
from langgraph_sdk import get_client
from src.model.chat import Message, MessageCreate, Thread, ThreadCreate, ThreadUpdate
from src.service.chat import ThreadBaseException
from src.web.user.dependencies import CurrentUser
from .dependencies import ThreadDBDependency
from src.web.dependencies import MessageDBDependency
from src.core.settings import get_settings

router = APIRouter(prefix="/threads", tags=["threads"])

settings = get_settings()
client = get_client(
    url=settings.LANGGRAPH_STREAM_URL, api_key=settings.LANGSMITH_API_KEY
)


@router.post("/", response_model=Thread)
async def create_thread(
    data: ThreadCreate,
    tdb: ThreadDBDependency,
    user: CurrentUser,
) -> Thread:
    user_id = None
    if user:
        user_id = user
    elif data.user_id:
        user_id = user

    if user_id is None:
        raise HTTPException(detail="user_id is required", status_code=400)
    return await tdb.create_thread(
        thread_id=data.thread_id,
        user_id=user_id,
        course_id=data.course_id,
        title=data.title,
        agent=data.agent,
    )


@router.get("/", response_model=list[Thread])
async def list_my_threads(
    tdb: ThreadDBDependency,
    user: CurrentUser,
) -> list[Thread]:
    return await tdb.list_threads_for_user(
        user_id=user,
    )


@router.post("/{thread_id}/messages", response_model=Message)
async def create_message(
    thread_id: UUID | str,
    data: MessageCreate,
    mdb: MessageDBDependency,
    tdb: ThreadDBDependency,
) -> Message:
    try:
        msg = await mdb.create_message(
            thread_id=thread_id,
            role=data.role,
            content=data.content,
        )
        await tdb.touch_updated_at(thread_id)
        return msg
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to create the message {e}",
        )


@router.get("/{thread_id}/messages", response_model=Thread)
async def get_messages(
    thread_id: UUID | str,
    tdb: ThreadDBDependency,
):
    try:
        await tdb.get_thread(thread_id)

        data = await client.threads.get(str(thread_id))
        values = data.get("values", {}) if isinstance(data, dict) else {}
        messages = values.get("messages", [])  # type: ignore
        return messages if isinstance(messages, list) else []
    except ThreadBaseException as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Failed to retrieve thread {thread_id} {e}",
        ) from e
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_502_BAD_GATEWAY,
            detail=f"Failed to retrieve thread data from stream service: {e}",
        ) from e


@router.get("/{thread_id}")
async def get_thread(thread_id: str | UUID, tdb: ThreadDBDependency) -> Thread:
    try:
        return await tdb.get_thread(thread_id)
    except ThreadBaseException as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Failed to get thread  {thread_id} {e}",
        ) from e
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Thread error internal: {e}",
        ) from e


@router.put("/{thread_id}")
async def update_thread(
    thread_id: str | UUID, tdb: ThreadDBDependency, thread_update: ThreadUpdate
) -> Thread:
    try:
        return await tdb.update_thread(thread_id, thread_update)
    except ThreadBaseException as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Failed to update thread  {thread_id} {e}",
        ) from e
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Thread error internal: {e}",
        ) from e


# @router.get("/{thread_id}/messages", response_model=list[Message])
# async def list_messages(
#     thread_id: UUID,
#     mdb: MessageDBDependency,
#     user: CurrentUser,
# ) -> list[Message]:
#     return await mdb.list_messages(thread_id)

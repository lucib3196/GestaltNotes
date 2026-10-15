from datetime import datetime
from typing import Never
from unittest.mock import AsyncMock, MagicMock
from uuid import uuid4

import pytest
from sqlalchemy.exc import SQLAlchemyError
from sqlmodel import Session

from backend.chat import (
    ThreadCreateError,
    ThreadNotFound,
    ThreadRetrievalError,
    ThreadService,
    ThreadUpdateError,
)
from backend.chat.model import Thread


def raise_error(*args, **kwargs) -> Never:
    raise SQLAlchemyError("db error")


@pytest.fixture
def mock_session():
    return MagicMock()


@pytest.fixture
def db(mock_session: Session) -> ThreadService:
    return ThreadService(session=mock_session, client=MagicMock())


@pytest.fixture
def sample_thread():
    return Thread(
        id=uuid4(),
        user_id=uuid4(),
        title="testing thread",
        agent="user",
        created_at=datetime.utcnow(),
        updated_at=datetime.utcnow(),
    )


@pytest.mark.asyncio
async def test_create_thread(db: ThreadService, mock_session: MagicMock) -> None:
    user_id = uuid4()
    uuid4()

    result = await db.create_thread(
        user_id=user_id,
        title="thread",
        agent="user",
    )

    mock_session.add.assert_called_once()
    mock_session.commit.assert_called_once()
    mock_session.flush.assert_called_once()

    assert result.user_id == user_id
    assert result.title == "thread"
    assert result.agent == "user"


@pytest.mark.asyncio
async def test_create_thread_optional_fields_blank(db: ThreadService) -> None:
    result = await db.create_thread(user_id=uuid4())

    assert result.title is None
    assert result.agent is None


@pytest.mark.asyncio
async def test_create_thread_error_and_rollback(
    db: ThreadService, mock_session
) -> None:

    mock_session.commit = raise_error

    with pytest.raises(
        ThreadCreateError, match=r"\[ThreadService\] failed to create thread"
    ):
        await db.create_thread(user_id=uuid4())

    mock_session.rollback.assert_called_once()


@pytest.mark.asyncio
async def test_get_thread(db: ThreadService, mock_session, sample_thread) -> None:
    mock_session.exec.return_value.first.return_value = sample_thread

    result = await db.get_thread(sample_thread.id)

    assert result == sample_thread
    mock_session.exec.assert_called_once()


@pytest.mark.asyncio
async def test_get_thread_not_found(db: ThreadService, mock_session) -> None:
    mock_session.exec.return_value.first.return_value = None
    missing_id = uuid4()

    with pytest.raises(ThreadNotFound, match=str(missing_id)):
        await db.get_thread(missing_id)


@pytest.mark.asyncio
async def test_get_thread_error_and_rollback(
    db: ThreadService, mock_session: MagicMock
) -> None:

    mock_session.exec = raise_error

    with pytest.raises(
        ThreadRetrievalError, match=r"\[ThreadService\] failed to get thread"
    ):
        await db.get_thread(uuid4())

    mock_session.rollback.assert_called_once()


@pytest.mark.asyncio
async def test_list_threads_returns_all_for_user(
    db: ThreadService, mock_session, sample_thread
) -> None:
    mock_session.exec.return_value.all.return_value = [sample_thread]

    result = await db.list_threads_for_user(user_id=sample_thread.user_id)

    assert result == [sample_thread]
    mock_session.exec.assert_called_once()


@pytest.mark.asyncio
async def test_list_threads_empty(db: ThreadService, mock_session: MagicMock) -> None:
    mock_session.exec.return_value.all.return_value = []

    result = await db.list_threads_for_user(user_id=uuid4())

    assert result == []


@pytest.mark.asyncio
async def test_list_threads_error_and_rollback(
    db: ThreadService, mock_session: MagicMock
) -> None:
    mock_session.exec = raise_error

    with pytest.raises(
        ThreadRetrievalError, match=r"\[ThreadService\] failed to list threads"
    ):
        await db.list_threads_for_user(user_id=uuid4())

    mock_session.rollback.assert_called_once()


@pytest.mark.asyncio
async def test_touch_updated_at(
    db: ThreadService, mock_session: MagicMock, sample_thread
) -> None:
    original_time = sample_thread.updated_at
    mock_session.exec.return_value.first.return_value = sample_thread

    result = await db.touch_updated_at(sample_thread.user_id, sample_thread.id)

    assert result.updated_at > original_time
    mock_session.add.assert_called_once_with(sample_thread)
    mock_session.commit.assert_called_once()


@pytest.mark.asyncio
async def test_touch_updated_at_error(
    db: ThreadService, mock_session: MagicMock
) -> None:
    mock_session.exec.return_value.first.return_value = None

    with pytest.raises(ThreadNotFound):
        await db.touch_updated_at(uuid4(), uuid4())


@pytest.mark.asyncio
async def test_touch_updated_at_rolls_back(
    db: ThreadService, mock_session: MagicMock, sample_thread
) -> None:
    mock_session.exec.return_value.first.return_value = sample_thread
    mock_session.commit = raise_error

    with pytest.raises(ThreadUpdateError, match="Failed to update thread timestamp"):
        await db.touch_updated_at(sample_thread.user_id, sample_thread.id)

    mock_session.rollback.assert_called_once()


@pytest.mark.asyncio
async def test_assert_owner_scopes_query(db, mock_session, sample_thread):
    mock_session.exec.return_value.first.return_value = sample_thread
    result = await db.assert_thread_owner(sample_thread.user_id, sample_thread.id)
    assert result is sample_thread
    stmt = mock_session.exec.call_args.args[0]
    params = stmt.compile().params
    assert sample_thread.id in params.values()
    assert sample_thread.user_id in params.values()


@pytest.mark.asyncio
async def test_rejected_owner_prevents_external_read_and_update(db, mock_session):
    mock_session.exec.return_value.first.return_value = None
    db.client.threads.get = AsyncMock()
    from backend.chat.schema import ThreadUpdate

    with pytest.raises(ThreadNotFound):
        await db.get_messages(uuid4(), uuid4())
    with pytest.raises(ThreadNotFound):
        await db.update_thread(uuid4(), uuid4(), ThreadUpdate(title="changed"))
    db.client.threads.get.assert_not_awaited()
    mock_session.commit.assert_not_called()


@pytest.mark.asyncio
async def test_get_messages_preserves_langgraph_payload(
    db, mock_session, sample_thread
):
    mock_session.exec.return_value.first.return_value = sample_thread
    messages = [{"type": "human", "content": [{"type": "text", "text": "Hi"}]}]
    db.client.threads.get = AsyncMock(return_value={"values": {"messages": messages}})
    assert await db.get_messages(sample_thread.user_id, sample_thread.id) == messages
    db.client.threads.get.assert_awaited_once_with(str(sample_thread.id))


@pytest.mark.asyncio
@pytest.mark.parametrize("values", [None, {}, {"messages": []}])
async def test_get_messages_empty_state(db, mock_session, sample_thread, values):
    mock_session.exec.return_value.first.return_value = sample_thread
    db.client.threads.get = AsyncMock(return_value={"values": values})
    assert await db.get_messages(sample_thread.user_id, sample_thread.id) == []


@pytest.mark.asyncio
@pytest.mark.parametrize("values", [[], {"messages": "bad"}, {"messages": [1]}])
async def test_get_messages_invalid_state(db, mock_session, sample_thread, values):
    from backend.chat import ThreadMessageRetrievalError

    mock_session.exec.return_value.first.return_value = sample_thread
    db.client.threads.get = AsyncMock(return_value={"values": values})
    with pytest.raises(ThreadMessageRetrievalError):
        await db.get_messages(sample_thread.user_id, sample_thread.id)


@pytest.mark.asyncio
async def test_get_messages_upstream_failure(db, mock_session, sample_thread):
    from backend.chat import ThreadMessageRetrievalError

    mock_session.exec.return_value.first.return_value = sample_thread
    db.client.threads.get = AsyncMock(side_effect=RuntimeError("private detail"))
    with pytest.raises(ThreadMessageRetrievalError, match="Failed to retrieve"):
        await db.get_messages(sample_thread.user_id, sample_thread.id)


@pytest.mark.asyncio
@pytest.mark.parametrize("title", ["new", "", None])
async def test_update_title_and_timestamp(db, mock_session, sample_thread, title):
    from backend.chat.schema import ThreadUpdate

    mock_session.exec.return_value.first.return_value = sample_thread
    previous_time = sample_thread.updated_at
    result = await db.update_thread(
        sample_thread.user_id, sample_thread.id, ThreadUpdate(title=title)
    )
    assert result.title == title
    assert result.updated_at > previous_time
    mock_session.commit.assert_called_once()


@pytest.mark.asyncio
async def test_delete_order(db, mock_session, sample_thread):
    mock_session.exec.return_value.first.return_value = sample_thread
    events = []
    mock_session.flush.side_effect = lambda: events.append("sql")
    mock_session.commit.side_effect = lambda: events.append("commit")

    async def remote_delete(thread_id):
        assert thread_id == str(sample_thread.id)
        events.append("remote")

    db.client.threads.delete = AsyncMock(side_effect=remote_delete)
    await db.delete_thread(sample_thread.user_id, sample_thread.id)
    assert events == ["sql", "remote", "commit"]
    mock_session.rollback.assert_not_called()


@pytest.mark.asyncio
async def test_delete_unowned_thread(db, mock_session):
    mock_session.exec.return_value.first.return_value = None
    db.client.threads.delete = AsyncMock()
    with pytest.raises(ThreadNotFound):
        await db.delete_thread(uuid4(), uuid4())
    db.client.threads.delete.assert_not_awaited()
    mock_session.commit.assert_not_called()
    assert mock_session.exec.call_count == 1


@pytest.mark.asyncio
@pytest.mark.parametrize("stage", ["sql", "remote", "commit"])
async def test_delete_failure_rolls_back(db, mock_session, sample_thread, stage):
    from backend.chat import (
        ThreadClientDeleteError,
        ThreadDeleteCommitError,
        ThreadDeleteError,
    )

    mock_session.exec.return_value.first.return_value = sample_thread
    db.client.threads.delete = AsyncMock()
    error_type = ThreadDeleteError
    if stage == "sql":
        mock_session.flush.side_effect = SQLAlchemyError("private")
    elif stage == "remote":
        db.client.threads.delete.side_effect = RuntimeError("private")
        error_type = ThreadClientDeleteError
    else:
        mock_session.commit.side_effect = SQLAlchemyError("private")
        error_type = ThreadDeleteCommitError
    with pytest.raises(error_type):
        await db.delete_thread(sample_thread.user_id, sample_thread.id)
    mock_session.rollback.assert_called_once()
    if stage == "sql":
        db.client.threads.delete.assert_not_awaited()
    if stage != "commit":
        mock_session.commit.assert_not_called()


@pytest.mark.asyncio
async def test_delete_remote_already_absent(db, mock_session, sample_thread):
    from httpx import HTTPStatusError, Request, Response

    mock_session.exec.return_value.first.return_value = sample_thread
    request = Request("DELETE", "http://test/threads/example")
    db.client.threads.delete = AsyncMock(
        side_effect=HTTPStatusError(
            "gone", request=request, response=Response(404, request=request)
        )
    )
    await db.delete_thread(sample_thread.user_id, sample_thread.id)
    mock_session.commit.assert_called_once()
    mock_session.rollback.assert_not_called()


@pytest.mark.asyncio
@pytest.mark.parametrize("remote_fails", [False, True])
async def test_delete_sql_rows_and_restore_on_failure(db_session, remote_fails):
    from backend.accounts.models import User
    from backend.chat import ThreadClientDeleteError
    from backend.chat.model import Message

    user = User(email="delete-test@example.com")
    db_session.add(user)
    db_session.commit()
    thread = Thread(user_id=user.id, title="Delete me")
    db_session.add(thread)
    db_session.commit()
    thread_id = thread.id
    message = Message(thread_id=thread_id, role="user", content="Hello")
    db_session.add(message)
    db_session.commit()
    message_id = message.id
    client = MagicMock()

    async def remote_delete(_thread_id):
        assert db_session.get(Thread, thread_id) is None
        assert db_session.get(Message, message_id) is None
        if remote_fails:
            raise RuntimeError("offline")

    client.threads.delete = AsyncMock(side_effect=remote_delete)
    service = ThreadService(db_session, client)
    if remote_fails:
        with pytest.raises(ThreadClientDeleteError):
            await service.delete_thread(user.id, thread_id)
    else:
        await service.delete_thread(user.id, thread_id)
    assert (db_session.get(Thread, thread_id) is not None) == remote_fails
    assert (db_session.get(Message, message_id) is not None) == remote_fails

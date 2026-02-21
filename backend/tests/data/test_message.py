import pytest
from unittest.mock import MagicMock
from uuid import uuid4
from datetime import datetime
from sqlalchemy.exc import SQLAlchemyError
from src.data.message import MessageDB
from src.model.chat import Message

def raise_error(*args, **kwargs):
    raise SQLAlchemyError("db error")

@pytest.fixture
def mock_session():
    return MagicMock()

@pytest.fixture
def db(mock_session):
    return MessageDB(session=mock_session)

@pytest.fixture
def sample_message():
    return Message(
        id=uuid4(),
        thread_id=uuid4(),
        role="user",
        content="Hello!",
        created_at=datetime.utcnow(),
    )

@pytest.mark.asyncio
async def test_create_message(db, mock_session):
    thread_id = uuid4()

    result = await db.create_message(
        thread_id=thread_id,
        role="user",
        content="Hello, World!",
    )

    mock_session.add.assert_called_once()
    mock_session.commit.assert_called_once()
    mock_session.flush.assert_called_once()

    assert result.thread_id == thread_id
    assert result.role == "user"
    assert result.content == "Hello, World!"

@pytest.mark.asyncio
async def test_create_message_error_and_rollback(db, mock_session):
    mock_session.commit = raise_error

    with pytest.raises(ValueError, match=r"\[MessageDB\] failed to create message"):
        await db.create_message(thread_id=uuid4(), role="ai bot", content="meow i am cat")

    mock_session.rollback.assert_called_once()

@pytest.mark.asyncio
async def test_get_message(db, mock_session, sample_message):
    mock_session.exec.return_value.first.return_value = sample_message

    result = await db.get_message(sample_message.id)

    assert result == sample_message
    mock_session.exec.assert_called_once()

@pytest.mark.asyncio
async def test_get_message_not_found(db, mock_session):
    mock_session.exec.return_value.first.return_value = None
    missing_id = uuid4()

    with pytest.raises(ValueError, match=str(missing_id)):
        await db.get_message(missing_id)

@pytest.mark.asyncio
async def test_get_message_error_and_rollback(db, mock_session):
    mock_session.exec = raise_error

    with pytest.raises(ValueError, match=r"\[MessageDB\] failed to get message"):
        await db.get_message(uuid4())

    mock_session.rollback.assert_called_once()

@pytest.mark.asyncio
async def test_list_messages(db, mock_session, sample_message):
    mock_session.exec.return_value.all.return_value = [sample_message]

    result = await db.list_messages(thread_id=sample_message.thread_id)

    assert result == [sample_message]
    mock_session.exec.assert_called_once()

@pytest.mark.asyncio
async def test_list_messages_empty(db, mock_session):
    mock_session.exec.return_value.all.return_value = []

    result = await db.list_messages(thread_id=uuid4())

    assert result == []

@pytest.mark.asyncio
async def test_list_messages_ordered_by_created_at(db, mock_session):
    mock_session.exec.return_value.all.return_value = []

    await db.list_messages(thread_id=uuid4())

    stmt = mock_session.exec.call_args[0][0]
    compiled = str(stmt.compile(compile_kwargs={"literal_binds": True}))
    assert "created_at" in compiled
    assert "ASC" in compiled

@pytest.mark.asyncio
async def test_list_messages_filters_by_thread_id(db, mock_session, sample_message):
    mock_session.exec.return_value.all.return_value = [sample_message]

    await db.list_messages(thread_id=sample_message.thread_id)

    stmt = mock_session.exec.call_args[0][0]
    compiled = str(stmt.compile(compile_kwargs={"literal_binds": True}))
    where_clause = compiled.split("WHERE")[1]
    assert "thread_id" in where_clause

@pytest.mark.asyncio
async def test_list_messages_error_and_rollback(db, mock_session):
    mock_session.exec = raise_error

    with pytest.raises(ValueError, match=r"\[MessageDB\] failed to list messages"):
        await db.list_messages(thread_id=uuid4())

    mock_session.rollback.assert_called_once()
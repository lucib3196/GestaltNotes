import pytest
from unittest.mock import MagicMock
from uuid import uuid4
from datetime import datetime
from sqlalchemy.exc import SQLAlchemyError
from src.data.thread import ThreadDB
from src.model.chat import Thread

def raise_error(*args, **kwargs):
    raise SQLAlchemyError("db error")

@pytest.fixture
def mock_session():
    return MagicMock()

@pytest.fixture
def db(mock_session):
    return ThreadDB(session=mock_session)

@pytest.fixture
def sample_thread():
    return Thread(
        id=uuid4(),
        user_id=uuid4(),
        course_id=uuid4(),
        title="testing thread",
        agent="user",
        created_at=datetime.utcnow(),
        updated_at=datetime.utcnow(),
    )

@pytest.mark.asyncio
async def test_create_thread(db, mock_session):
    user_id = uuid4()
    course_id = uuid4()

    result = await db.create_thread(
        user_id=user_id,
        course_id=course_id,
        title="thread",
        agent="user",
    )

    mock_session.add.assert_called_once()
    mock_session.commit.assert_called_once()
    mock_session.flush.assert_called_once()

    assert result.user_id == user_id
    assert result.course_id == course_id
    assert result.title == "thread"
    assert result.agent == "user"

@pytest.mark.asyncio
async def test_create_thread_optional_fields_blank(db):
    result = await db.create_thread(user_id=uuid4(), course_id=uuid4())

    assert result.title is None
    assert result.agent is None

@pytest.mark.asyncio
async def test_create_thread_error_and_rollback(db, mock_session):

    mock_session.commit = raise_error

    with pytest.raises(ValueError, match=r"\[ThreadDB\] failed to create thread"):
        await db.create_thread(user_id=uuid4(), course_id=uuid4())

    mock_session.rollback.assert_called_once()

@pytest.mark.asyncio
async def test_get_thread(db, mock_session, sample_thread):
    mock_session.exec.return_value.first.return_value = sample_thread

    result = await db.get_thread(sample_thread.id)

    assert result == sample_thread
    mock_session.exec.assert_called_once()

@pytest.mark.asyncio
async def test_get_thread_not_found(db, mock_session):
    mock_session.exec.return_value.first.return_value = None
    missing_id = uuid4()

    with pytest.raises(ValueError, match=str(missing_id)):
        await db.get_thread(missing_id)

@pytest.mark.asyncio
async def test_get_thread_error_and_rollback(db, mock_session):

    mock_session.exec = raise_error

    with pytest.raises(ValueError, match=r"\[ThreadDB\] failed to get thread"):
        await db.get_thread(uuid4())

    mock_session.rollback.assert_called_once()

@pytest.mark.asyncio
async def test_list_threads_returns_all_for_user(db, mock_session, sample_thread):
    mock_session.exec.return_value.all.return_value = [sample_thread]

    result = await db.list_threads_for_user(user_id=sample_thread.user_id)

    assert result == [sample_thread]
    mock_session.exec.assert_called_once()

@pytest.mark.asyncio
async def test_list_threads_filters(db, mock_session, sample_thread):
    mock_session.exec.return_value.all.return_value = [sample_thread]

    result = await db.list_threads_for_user(
        user_id=sample_thread.user_id,
        course_id=sample_thread.course_id,
    )

    assert result == [sample_thread]

@pytest.mark.asyncio
async def test_list_threads_filters_by_course_id(db, mock_session, sample_thread):
    mock_session.exec.return_value.all.return_value = [sample_thread]

    result = await db.list_threads_for_user(
        user_id=sample_thread.user_id,
        course_id=sample_thread.course_id,
    )

    assert result == [sample_thread]
    stmt = mock_session.exec.call_args[0][0]
    compiled = str(stmt.compile(compile_kwargs={"literal_binds": True}))
    assert "user_id" in compiled
    assert "course_id" in compiled

@pytest.mark.asyncio
async def test_list_threads_empty(db, mock_session):
    mock_session.exec.return_value.all.return_value = []

    result = await db.list_threads_for_user(user_id=uuid4())

    assert result == []

@pytest.mark.asyncio
async def test_list_threads_no_course_id(db, mock_session):
    mock_session.exec.return_value.all.return_value = []

    await db.list_threads_for_user(user_id=uuid4(), course_id=None)

    stmt = mock_session.exec.call_args[0][0]
    compiled = str(stmt.compile(compile_kwargs={"literal_binds": True}))
    assert "WHERE" in compiled
    where_clause = compiled.split("WHERE")[1]
    assert "course_id" not in where_clause

@pytest.mark.asyncio
async def test_list_threads_error_and_rollback(db, mock_session):
    mock_session.exec = raise_error

    with pytest.raises(ValueError, match=r"\[ThreadDB\] failed to list threads"):
        await db.list_threads_for_user(user_id=uuid4())

    mock_session.rollback.assert_called_once()

@pytest.mark.asyncio
async def test_touch_updated_at(db, mock_session, sample_thread):
    original_time = sample_thread.updated_at
    mock_session.exec.return_value.first.return_value = sample_thread

    result = await db.touch_updated_at(sample_thread.id)

    assert result.updated_at > original_time
    mock_session.add.assert_called_once_with(sample_thread)
    mock_session.commit.assert_called_once()
    mock_session.flush.assert_called_once()

@pytest.mark.asyncio
async def test_touch_updated_at_error(db, mock_session):
    mock_session.exec.return_value.first.return_value = None

    with pytest.raises(ValueError):
        await db.touch_updated_at(uuid4())

@pytest.mark.asyncio
async def test_touch_updated_at_rolls_back(db, mock_session, sample_thread):
    mock_session.exec.return_value.first.return_value = sample_thread
    mock_session.commit = raise_error

    with pytest.raises(ValueError, match=r"\[ThreadDB\] failed to update thread timestamp"):
        await db.touch_updated_at(sample_thread.id)

    mock_session.rollback.assert_called_once()
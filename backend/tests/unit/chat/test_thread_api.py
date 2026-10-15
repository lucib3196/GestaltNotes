from unittest.mock import AsyncMock
from uuid import uuid4

import pytest
from fastapi import FastAPI
from httpx import ASGITransport, AsyncClient

from backend.chat import ThreadMessageRetrievalError, ThreadNotFound, ThreadService
from backend.web.accounts.dependencies import get_current_user_id
from backend.web.chat.dependencies import get_thread_service
from backend.web.chat.thread import router
from backend.web.dependencies import get_message_db


@pytest.fixture
async def api():
    app = FastAPI()
    app.include_router(router)
    service = AsyncMock(spec=ThreadService)
    messages = AsyncMock()

    async def provide_service():
        return service

    async def provide_messages():
        return messages

    app.dependency_overrides[get_thread_service] = provide_service
    app.dependency_overrides[get_message_db] = provide_messages
    async with AsyncClient(
        transport=ASGITransport(app=app), base_url="http://test"
    ) as client:
        yield client, app, service, messages


@pytest.mark.parametrize(
    ("method", "suffix", "body"),
    [
        ("get", "", None),
        ("delete", "", None),
        ("put", "", {"title": "new"}),
        ("get", "/messages", None),
        ("post", "/messages", {"role": "user", "content": "Hi"}),
    ],
)
async def test_thread_operations_require_auth(api, method, suffix, body):
    client, _, service, messages = api
    kwargs = {"json": body} if body is not None else {}
    response = await client.request(method, f"/threads/{uuid4()}{suffix}", **kwargs)
    assert response.status_code == 401
    assert not service.mock_calls
    assert not messages.mock_calls


async def test_message_response_and_authenticated_owner(api):
    client, app, service, _ = api
    user_id, thread_id = str(uuid4()), uuid4()

    async def current_user():
        return user_id

    app.dependency_overrides[get_current_user_id] = current_user
    payload = [{"type": "human", "content": "Hi"}]
    service.get_messages.return_value = payload
    response = await client.get(f"/threads/{thread_id}/messages")
    assert response.status_code == 200
    assert response.json() == payload
    service.get_messages.assert_awaited_once_with(user_id, thread_id)


@pytest.mark.parametrize(
    ("error", "status"),
    [(ThreadNotFound("private"), 404), (ThreadMessageRetrievalError("private"), 502)],
)
async def test_message_errors_have_public_details(api, error, status):
    client, app, service, _ = api

    async def current_user():
        return str(uuid4())

    app.dependency_overrides[get_current_user_id] = current_user
    service.get_messages.side_effect = error
    response = await client.get(f"/threads/{uuid4()}/messages")
    assert response.status_code == status
    assert "private" not in response.text


async def test_unowned_thread_cannot_receive_message(api):
    client, app, service, messages = api

    async def current_user():
        return str(uuid4())

    app.dependency_overrides[get_current_user_id] = current_user
    service.assert_thread_owner.side_effect = ThreadNotFound()
    response = await client.post(
        f"/threads/{uuid4()}/messages", json={"role": "user", "content": "Hi"}
    )
    assert response.status_code == 404
    messages.create_message.assert_not_awaited()


async def test_delete_success(api):
    client, app, service, _ = api
    user_id, thread_id = str(uuid4()), uuid4()

    async def current_user():
        return user_id

    app.dependency_overrides[get_current_user_id] = current_user
    response = await client.delete(f"/threads/{thread_id}")
    assert response.status_code == 204
    assert response.content == b""
    service.delete_thread.assert_awaited_once_with(user_id, thread_id)


@pytest.mark.parametrize("failure", ["missing", "sql", "remote", "commit"])
async def test_delete_error_mapping(api, failure):
    from backend.chat import (
        ThreadClientDeleteError,
        ThreadDeleteCommitError,
        ThreadDeleteError,
    )

    client, app, service, _ = api

    async def current_user():
        return str(uuid4())

    app.dependency_overrides[get_current_user_id] = current_user
    errors = {
        "missing": (ThreadNotFound, 404),
        "sql": (ThreadDeleteError, 500),
        "remote": (ThreadClientDeleteError, 502),
        "commit": (ThreadDeleteCommitError, 500),
    }
    error_type, status = errors[failure]
    service.delete_thread.side_effect = error_type("private")
    response = await client.delete(f"/threads/{uuid4()}")
    assert response.status_code == status
    assert "private" not in response.text

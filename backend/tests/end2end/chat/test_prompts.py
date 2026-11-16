from types import SimpleNamespace
from uuid import UUID, uuid4

import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient

from backend.accounts.models import User, UserRole
from backend.database import get_session
from backend.web import ALL_ROUTES
from backend.web.accounts.dependencies import get_current_user
from backend.web.chat.prompts import router as prompt_router


@pytest.fixture
def api(db_session):
    # Add users
    reader = User(email=f"reader-{uuid4().hex}@example.com")
    outsider = User(email=f"outsider-{uuid4().hex}@example.com")
    db_session.add_all([reader, outsider])
    db_session.commit()

    app = FastAPI()
    app.include_router(prompt_router)

    ## Overrides for dependency
    def session_override():
        yield db_session

    def current_user_override():
        user = db_session.get(User, reader.id)
        return SimpleNamespace(
            id=user.id, roles=[SimpleNamespace(name=UserRole.STUDENT)]
        )

    app.dependency_overrides[get_session] = session_override
    app.dependency_overrides[get_current_user] = current_user_override
    with TestClient(app) as client:
        yield SimpleNamespace(client=client, reader=reader, outsider=outsider)


def test_route_registered():
    assert prompt_router in ALL_ROUTES


def test_create_prompt(api):
    payload = {
        "title": "myTitle",
        "description": "MyPrompt",
        "content": "Some Content",
    }

    response = api.client.post("/prompts/", json=payload)

    assert response.status_code == 201, response.text
    prompt = response.json()
    assert UUID(prompt["id"])
    assert prompt["user_id"] == str(api.reader.id)
    for field, value in payload.items():
        assert prompt[field] == value

    saved = api.client.get(f"/prompts/{prompt['id']}")
    assert saved.status_code == 200, saved.text
    assert saved.json() == prompt


def test_list_prompts_empty(api):
    response = api.client.get("/prompts/")

    assert response.status_code == 200, response.text
    assert response.json() == []


def test_list_prompts(api):
    expected = []
    for title in ("First prompt", "Second prompt"):
        response = api.client.post(
            "/prompts/",
            json={
                "title": title,
                "description": f"Description for {title}",
                "content": "Some Content",
            },
        )
        assert response.status_code == 201, response.text
        prompt = response.json()
        expected.append(
            {
                "id": prompt["id"],
                "title": prompt["title"],
                "description": prompt["description"],
            }
        )

    response = api.client.get("/prompts/", params={"order": "asc"})

    assert response.status_code == 200, response.text
    assert response.json() == expected


def test_delete_prompt(api):
    created = api.client.post(
        "/prompts/",
        json={"title": "Delete me", "content": "Some Content"},
    )
    assert created.status_code == 201, created.text
    prompt_id = created.json()["id"]

    response = api.client.delete(f"/prompts/{prompt_id}")

    assert response.status_code == 204, response.text
    assert response.content == b""
    assert api.client.get(f"/prompts/{prompt_id}").status_code == 404

    listing = api.client.get("/prompts/")
    assert listing.status_code == 200, listing.text
    assert listing.json() == []


def test_delete_missing_prompt(api):
    response = api.client.delete(f"/prompts/{uuid4()}")

    assert response.status_code == 404, response.text

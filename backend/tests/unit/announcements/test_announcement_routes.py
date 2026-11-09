from types import SimpleNamespace
from uuid import uuid4

import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient
from sqlalchemy import event
from sqlmodel import SQLModel, create_engine, select

from backend.accounts.models import User, UserRole
from backend.announcements.models import Announcement, AnnouncementRecipient
from backend.database import get_session
from backend.web import ALL_ROUTES
from backend.web.accounts.dependencies import get_current_user
from backend.web.annoucements.admin import router as admin_router
from backend.web.annoucements.announcements import router as user_router


@pytest.fixture
def test_engine(tmp_path):
    # Share the database across TestClient and dependency worker threads.
    engine = create_engine(
        f"sqlite:///{tmp_path / 'announcements.db'}",
        connect_args={"check_same_thread": False},
    )

    @event.listens_for(engine, "connect")
    def enable_foreign_keys(connection, _):
        connection.execute("PRAGMA foreign_keys=ON")

    SQLModel.metadata.create_all(engine)
    yield engine
    engine.dispose()


@pytest.fixture
def api(db_session):
    admin = User(email=f"admin-{uuid4().hex}@example.com")
    reader = User(email=f"reader-{uuid4().hex}@example.com")
    outsider = User(email=f"outsider-{uuid4().hex}@example.com")
    db_session.add_all([admin, reader, outsider])
    db_session.commit()
    actor = SimpleNamespace(id=admin.id, admin=True)
    app = FastAPI()
    app.include_router(user_router)
    app.include_router(admin_router)

    def session_override():
        yield db_session

    def current_user_override():
        # Model authentication's database lookup and its active transaction.
        user = db_session.get(User, actor.id)
        return SimpleNamespace(
            id=user.id,
            roles=[SimpleNamespace(name=UserRole.ADMIN)] if actor.admin else [],
        )

    app.dependency_overrides[get_session] = session_override
    app.dependency_overrides[get_current_user] = current_user_override
    with TestClient(app) as client:
        yield SimpleNamespace(
            client=client, actor=actor, reader=reader, outsider=outsider
        )


def create_draft(api):
    response = api.client.post(
        "/admin/announcements/",
        json={"title": "Release", "message": "New features", "version": "1.2.0"},
    )
    assert response.status_code == 201, response.text
    return response.json()["id"]


def test_routers_registered():
    assert user_router in ALL_ROUTES
    assert admin_router in ALL_ROUTES


def test_publish_and_read_workflow(api, db_session):
    announcement_id = create_draft(api)
    base = f"/admin/announcements/{announcement_id}"
    recipients = {"user_ids": [str(api.reader.id)]}
    assert api.client.get(base).status_code == 200
    edited = api.client.patch(base, json={"message": "Updated features"})
    assert edited.status_code == 200
    assert edited.json()["title"] == "Release"
    added = api.client.post(f"{base}/recipients", json=recipients)
    assert added.status_code == 201, added.text
    assert len(api.client.get(f"{base}/recipients").json()) == 1
    assert api.client.post(f"{base}/publish").json()["published_at"] is not None

    api.actor.id, api.actor.admin = api.reader.id, False
    listed = api.client.get("/announcements/")
    assert listed.status_code == 200
    assert [item["id"] for item in listed.json()] == [announcement_id]
    user_base = f"/announcements/{announcement_id}"
    assert api.client.get(user_base).json()["message"] == "Updated features"
    read = api.client.put(f"{user_base}/read")
    assert read.status_code == 200
    assert read.json()["read_at"] is not None
    assert (
        api.client.put(f"{user_base}/read").json()["read_at"] == read.json()["read_at"]
    )
    db_session.expunge_all()
    assert db_session.exec(select(AnnouncementRecipient)).one().read_at is not None


def test_user_access_excludes_drafts_and_unassigned_announcements(api):
    announcement_id = create_draft(api)
    base = f"/admin/announcements/{announcement_id}"
    assert (
        api.client.post(
            f"{base}/recipients", json={"user_ids": [str(api.reader.id)]}
        ).status_code
        == 201
    )
    admin_id = api.actor.id
    api.actor.id, api.actor.admin = api.reader.id, False
    assert api.client.get("/announcements/").json() == []
    for method, suffix in [("GET", ""), ("PUT", "/read")]:
        assert (
            api.client.request(
                method, f"/announcements/{announcement_id}{suffix}"
            ).status_code
            == 404
        )
    api.actor.id, api.actor.admin = admin_id, True
    assert api.client.post(f"{base}/publish").status_code == 200
    api.actor.id, api.actor.admin = api.outsider.id, False
    assert api.client.get("/announcements/").json() == []
    assert api.client.get(f"/announcements/{announcement_id}").status_code == 404
    assert api.client.put(f"/announcements/{announcement_id}/read").status_code == 404


@pytest.mark.parametrize(
    ("method", "suffix"),
    [
        ("POST", "/"),
        ("GET", "/{id}"),
        ("PATCH", "/{id}"),
        ("POST", "/{id}/publish"),
        ("GET", "/{id}/audience-preview"),
        ("POST", "/{id}/publish-to-all"),
        ("DELETE", "/{id}"),
        ("GET", "/{id}/recipients"),
        ("POST", "/{id}/recipients"),
        ("DELETE", "/{id}/recipients"),
    ],
)
def test_admin_routes_reject_regular_users(api, method, suffix):
    api.actor.id, api.actor.admin = api.reader.id, False
    response = api.client.request(
        method,
        "/admin/announcements" + suffix.format(id=uuid4()),
        json={"title": "Title", "message": "Message", "version": "1", "user_ids": []},
    )
    assert response.status_code == 403


def test_missing_authentication():
    app = FastAPI()
    app.include_router(user_router)
    app.include_router(admin_router)
    with TestClient(app) as client:
        assert client.get("/announcements/").status_code == 401
        assert client.get(f"/admin/announcements/{uuid4()}").status_code == 401
        assert (
            client.get(f"/admin/announcements/{uuid4()}/audience-preview").status_code
            == 401
        )
        assert (
            client.post(f"/admin/announcements/{uuid4()}/publish-to-all").status_code
            == 401
        )


def test_recipient_retries_removal_and_delete(api, db_session):
    announcement_id = create_draft(api)
    base = f"/admin/announcements/{announcement_id}"
    recipients = {"user_ids": [str(api.reader.id)]}
    first = api.client.post(f"{base}/recipients", json=recipients)
    assert first.status_code == 201
    assert len(first.json()) == 1
    assert first.json()[0]["user_id"] == str(api.reader.id)

    repeated = api.client.post(f"{base}/recipients", json=recipients)
    assert repeated.status_code == 201
    assert repeated.json() == []

    missing = api.client.post(f"{base}/recipients", json={"user_ids": [str(uuid4())]})
    assert missing.status_code == 201
    assert missing.json() == []

    stored = api.client.get(f"{base}/recipients")
    assert stored.status_code == 200
    assert len(stored.json()) == 1
    assert stored.json()[0]["user_id"] == str(api.reader.id)
    assert (
        api.client.request("DELETE", f"{base}/recipients", json=recipients).status_code
        == 204
    )
    assert api.client.get(f"{base}/recipients").json() == []
    assert api.client.post(f"{base}/recipients", json=recipients).status_code == 201
    assert api.client.delete(base).status_code == 204
    assert db_session.exec(select(Announcement)).first() is None
    assert db_session.exec(select(AnnouncementRecipient)).first() is None
    assert api.client.delete(base).status_code == 404


@pytest.mark.parametrize("changes", [{"published": True}, {"title": None}])
def test_patch_rejects_publication_and_null_fields(api, changes):
    announcement_id = create_draft(api)
    assert (
        api.client.patch(
            f"/admin/announcements/{announcement_id}", json=changes
        ).status_code
        == 422
    )


def test_create_rejects_published_announcement(api):
    response = api.client.post(
        "/admin/announcements/",
        json={
            "title": "Title",
            "message": "Message",
            "version": "1",
            "published": True,
        },
    )
    assert response.status_code == 422


@pytest.mark.parametrize(
    ("method", "suffix", "body"),
    [
        ("GET", "", None),
        ("PATCH", "", {"message": "Updated"}),
        ("POST", "/publish", None),
        ("GET", "/audience-preview", None),
        ("POST", "/publish-to-all", None),
        ("GET", "/recipients", None),
        ("POST", "/recipients", {"user_ids": []}),
        ("DELETE", "/recipients", {"user_ids": []}),
    ],
)
def test_missing_announcement_returns_404(api, method, suffix, body):
    response = api.client.request(
        method, f"/admin/announcements/{uuid4()}{suffix}", json=body
    )
    assert response.status_code == 404


def test_preview_and_publish_to_all_users(api):
    announcement_id = create_draft(api)
    base = f"/admin/announcements/{announcement_id}"
    added = api.client.post(
        f"{base}/recipients", json={"user_ids": [str(api.reader.id)]}
    )
    assert added.status_code == 201

    preview = api.client.get(f"{base}/audience-preview")
    assert preview.status_code == 200
    assert preview.json() == {
        "announcement_id": announcement_id,
        "published": False,
        "total_users": 3,
        "existing_recipients": 1,
        "new_recipients": 2,
        "read_recipients": 0,
        "unread_recipients": 1,
    }
    assert len(api.client.get(f"{base}/recipients").json()) == 1
    assert not api.client.get(base).json()["published"]

    published = api.client.post(f"{base}/publish-to-all")
    assert published.status_code == 200
    assert published.json()["published"]
    assert published.json()["published_at"] is not None
    assert len(api.client.get(f"{base}/recipients").json()) == 3

    repeated = api.client.post(f"{base}/publish-to-all")
    assert repeated.status_code == 409
    assert repeated.json()["detail"] == "Announcement is already published"

    api.actor.id, api.actor.admin = api.outsider.id, False
    assert [item["id"] for item in api.client.get("/announcements/").json()] == [
        announcement_id
    ]


@pytest.mark.parametrize(
    ("method", "suffix", "body"),
    [
        ("GET", "", None),
        ("PATCH", "", {"title": "Unauthorized"}),
        ("POST", "/publish", None),
        ("POST", "/publish-to-all", None),
        ("DELETE", "", None),
        ("GET", "/recipients", None),
        ("GET", "/audience-preview", None),
        ("POST", "/recipients", {"user_ids": []}),
        ("DELETE", "/recipients", {"user_ids": []}),
    ],
)
def test_other_admin_cannot_manage_announcement(api, method, suffix, body):
    announcement_id = create_draft(api)
    base = f"/admin/announcements/{announcement_id}"
    owner_id = api.actor.id
    assert api.client.get(base).json()["created_by_id"] == str(owner_id)
    api.actor.id = api.outsider.id

    response = api.client.request(method, base + suffix, json=body)

    assert response.status_code == 404
    api.actor.id = owner_id
    stored = api.client.get(base)
    assert stored.status_code == 200
    assert stored.json()["title"] == "Release"
    assert not stored.json()["published"]
    assert api.client.get(f"{base}/recipients").json() == []

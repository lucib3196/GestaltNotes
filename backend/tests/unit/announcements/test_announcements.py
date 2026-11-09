from uuid import uuid4

import pytest

from backend.accounts import User
from backend.announcements.models import AnnoucementUpdate, Announcement
from backend.announcements.service import AnnoucementService


@pytest.fixture
def service(db_session) -> AnnoucementService:
    return AnnoucementService(db_session)


@pytest.fixture
def users(db_session) -> list[User]:
    records = [
        User(
            first_name=f"user{i}",
            email=f"user{i}-{uuid4().hex}@example.com",
        )
        for i in range(1, 4)
    ]
    db_session.add_all(records)
    db_session.flush()
    return records


@pytest.fixture
def make_announcement(service):
    async def make(title="My First"):
        return await service.create(
            Announcement(
                title=title,
                message="First announcement on the app",
                version="1.2.0",
            )
        )

    return make


@pytest.mark.asyncio
async def test_create_announcement(make_announcement):
    created = await make_announcement()

    assert created.title == "My First"
    assert created.message == "First announcement on the app"
    assert created.version == "1.2.0"
    assert not created.published
    assert created.published_at is None


@pytest.mark.asyncio
async def test_announcement_update(service, make_announcement):
    announcement = await make_announcement()

    updated = await service.update(
        announcement.id,
        AnnoucementUpdate(
            published=True,
            message="First announcement plus some updates",
        ),
    )

    assert updated.published
    assert updated.title == "My First"
    assert updated.message == "First announcement plus some updates"


@pytest.mark.asyncio
async def test_publish(service, make_announcement):
    announcement = await make_announcement()

    published = await service.publish(announcement.id)

    assert published.published
    assert published.id == announcement.id
    assert published.published_at is not None


@pytest.mark.asyncio
async def test_adding_recipients(service, users, make_announcement):
    announcement = await make_announcement()
    user_ids = [user.id for user in users]

    targets = await service.add_recipients(announcement.id, user_ids)

    assert len(targets) == len(user_ids)
    assert {target.user_id for target in targets} == set(user_ids)
    assert all(target.read_at is None for target in targets)
    assert all(target.announcement_id == announcement.id for target in targets)


@pytest.mark.asyncio
async def test_listing_recipients(service, users, make_announcement):
    announcement = await make_announcement()
    user_ids = [user.id for user in users]
    await service.add_recipients(announcement.id, user_ids)

    targets = await service.list_recipients(announcement.id)

    assert len(targets) == len(user_ids)
    assert {target.user_id for target in targets} == set(user_ids)


@pytest.mark.asyncio
async def test_remove_recipients(service, users, make_announcement):
    announcement = await make_announcement()
    user_ids = [user.id for user in users]
    await service.add_recipients(announcement.id, user_ids)

    await service.remove_recipients(announcement.id, user_ids)

    assert await service.list_recipients(announcement.id) == []


@pytest.mark.asyncio
async def test_list_announcements_for_user(service, users, make_announcement):
    assigned = await make_announcement("Assigned")
    other = await make_announcement("Another user's")
    draft = await make_announcement("Draft")

    await service.add_recipients(assigned.id, [users[0].id, users[1].id])
    await service.add_recipients(other.id, [users[1].id])
    await service.add_recipients(draft.id, [users[0].id])
    await service.publish(assigned.id)
    await service.publish(other.id)

    announcements = await service.list_announcements_for_user(users[0].id)

    assert [announcement.id for announcement in announcements] == [assigned.id]
    assert await service.list_announcements_for_user(users[2].id) == []


@pytest.mark.asyncio
async def test_mark_announcement_read(service, users, make_announcement, db_session):
    announcement = await make_announcement()
    announcement_id = announcement.id
    user_id, other_user_id = users[0].id, users[1].id
    await service.add_recipients(announcement_id, [user_id, other_user_id])
    await service.publish(announcement_id)

    recipient = await service.mark_announcement_read(user_id, announcement_id)
    first_read_at = recipient.read_at
    assert first_read_at is not None

    db_session.expunge_all()
    stored = await service.retrieve_annoucement_for_user(user_id, announcement_id)
    assert stored.read_at == first_read_at

    repeated = await service.mark_announcement_read(user_id, announcement_id)
    assert repeated.read_at == first_read_at

    other = await service.retrieve_annoucement_for_user(other_user_id, announcement_id)
    assert other.read_at is None


@pytest.mark.asyncio
async def test_mark_announcement_read_rejects_unassigned_user(
    service, users, make_announcement
):
    announcement = await make_announcement()
    await service.add_recipients(announcement.id, [users[0].id])

    with pytest.raises(ValueError, match="Failed to retrieve"):
        await service.mark_announcement_read(users[1].id, announcement.id)

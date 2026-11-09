from uuid import uuid4

import pytest

from backend.accounts import User
from backend.accounts.models import UserRole
from backend.announcements.management_service import AnnouncementManagementService
from backend.announcements.models import AnnoucementUpdate, Announcement
from backend.announcements.user_service import UserAnnouncementService


@pytest.fixture
async def admin(make_user) -> User:
    return await make_user(
        role=UserRole.ADMIN,
        first_name="admin",
    )


@pytest.fixture
def management_service(db_session, admin) -> AnnouncementManagementService:
    return AnnouncementManagementService(db_session, admin)


@pytest.fixture
def user_service(db_session) -> UserAnnouncementService:
    return UserAnnouncementService(db_session)


@pytest.fixture
async def users(make_user) -> list[User]:
    return [
        await make_user(
            first_name=f"user{i}",
            email=f"user{i}-{uuid4().hex}@example.com",
            role=UserRole.STUDENT,
        )
        for i in range(1, 4)
    ]


@pytest.fixture
def make_announcement(management_service):
    async def make(title="My First"):
        return await management_service.create(
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
async def test_announcement_update(management_service, make_announcement):
    announcement = await make_announcement()

    updated = await management_service.update(
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
async def test_publish(management_service, make_announcement):
    announcement = await make_announcement()

    published = await management_service.publish(announcement.id)

    assert published.published
    assert published.id == announcement.id
    assert published.published_at is not None


@pytest.mark.asyncio
async def test_adding_recipients(management_service, users, make_announcement):
    announcement = await make_announcement()
    user_ids = [user.id for user in users]

    targets = await management_service.add_recipients(announcement.id, user_ids)

    assert len(targets) == len(user_ids)
    assert {target.user_id for target in targets} == set(user_ids)
    assert all(target.read_at is None for target in targets)
    assert all(target.announcement_id == announcement.id for target in targets)


@pytest.mark.asyncio
async def test_listing_recipients(management_service, users, make_announcement):
    announcement = await make_announcement()
    user_ids = [user.id for user in users]
    await management_service.add_recipients(announcement.id, user_ids)

    targets = await management_service.list_recipients(announcement.id)

    assert len(targets) == len(user_ids)
    assert {target.user_id for target in targets} == set(user_ids)


@pytest.mark.asyncio
async def test_remove_recipients(management_service, users, make_announcement):
    announcement = await make_announcement()
    user_ids = [user.id for user in users]
    await management_service.add_recipients(announcement.id, user_ids)

    await management_service.remove_recipients(announcement.id, user_ids)

    assert await management_service.list_recipients(announcement.id) == []


@pytest.mark.asyncio
async def test_list_announcements_for_user(
    user_service, management_service, users, make_announcement
):
    assigned = await make_announcement("Assigned")
    other = await make_announcement("Another user's")
    draft = await make_announcement("Draft")

    await management_service.add_recipients(assigned.id, [users[0].id, users[1].id])
    await management_service.add_recipients(other.id, [users[1].id])
    await management_service.add_recipients(draft.id, [users[0].id])
    await management_service.publish(assigned.id)
    await management_service.publish(other.id)

    announcements = await user_service.list_announcements_for_user(users[0].id)

    assert [announcement.id for announcement in announcements] == [assigned.id]
    assert await user_service.list_announcements_for_user(users[2].id) == []


@pytest.mark.asyncio
async def test_mark_announcement_read(
    user_service, management_service, users, make_announcement, db_session
):
    announcement = await make_announcement()
    announcement_id = announcement.id
    user_id, other_user_id = users[0].id, users[1].id
    await management_service.add_recipients(announcement_id, [user_id, other_user_id])
    await management_service.publish(announcement_id)

    recipient = await user_service.mark_announcement_read(user_id, announcement_id)
    first_read_at = recipient.read_at
    assert first_read_at is not None

    db_session.expunge_all()
    stored = await user_service.retrieve_annoucement_for_user(user_id, announcement_id)
    assert stored.read_at == first_read_at

    repeated = await user_service.mark_announcement_read(user_id, announcement_id)
    assert repeated.read_at == first_read_at

    other = await user_service.retrieve_annoucement_for_user(
        other_user_id, announcement_id
    )
    assert other.read_at is None


@pytest.mark.asyncio
async def test_mark_announcement_read_rejects_unassigned_user(
    user_service, management_service, users, make_announcement
):
    announcement = await make_announcement()
    await management_service.add_recipients(announcement.id, [users[0].id])

    with pytest.raises(ValueError, match="Failed to retrieve"):
        await user_service.mark_announcement_read(users[1].id, announcement.id)


@pytest.mark.asyncio
async def test_preview_all_users_does_not_change_audience(
    user_service, management_service, users, make_announcement, db_session
):
    announcement = await make_announcement()
    other = await make_announcement("Other")
    await management_service.add_recipients(announcement.id, [users[0].id, users[1].id])
    await management_service.add_recipients(other.id, [users[2].id])
    recipient = await user_service.mark_announcement_read(users[0].id, announcement.id)
    read_at = recipient.read_at

    preview = await management_service.preview_all_users(announcement.id)

    assert preview.announcement_id == announcement.id
    assert not preview.published
    assert preview.total_users == 4
    assert preview.existing_recipients == 2
    assert preview.new_recipients == 2
    assert preview.read_recipients == 1
    assert preview.unread_recipients == 1
    db_session.expire_all()
    assert not (await management_service.get(announcement.id)).published
    recipients = await management_service.list_recipients(announcement.id)
    assert {recipient.user_id for recipient in recipients} == {users[0].id, users[1].id}
    assert (
        await user_service.retrieve_annoucement_for_user(users[0].id, announcement.id)
    ).read_at == read_at


@pytest.mark.asyncio
async def test_publish_to_all_users_preserves_existing_recipients(
    user_service, management_service, users, make_announcement, db_session, admin
):
    announcement = await make_announcement()
    announcement_id = announcement.id
    await management_service.add_recipients(announcement_id, [users[0].id])
    first = await user_service.mark_announcement_read(users[0].id, announcement_id)
    read_at = first.read_at
    # A preview starts a transaction; publication must work in that session.
    await management_service.preview_all_users(announcement_id)

    published = await management_service.publish_to_all_users(announcement_id)

    assert published.published
    assert published.published_at is not None
    assert published.audience_summary == "All current users"
    db_session.expunge_all()
    assert (await management_service.get(announcement_id)).published
    recipients = await management_service.list_recipients(announcement_id)
    assert len(recipients) == 4
    assert {recipient.user_id for recipient in recipients} == {
        user.id for user in users
    } | {admin.id}
    assert (
        await user_service.retrieve_annoucement_for_user(users[0].id, announcement_id)
    ).read_at == read_at
    for user in users:
        assert [
            item.id for item in await user_service.list_announcements_for_user(user.id)
        ] == [announcement_id]


@pytest.mark.asyncio
async def test_publish_all_users_uses_current_audience_and_rejects_republication(
    user_service, management_service, users, make_announcement, db_session, admin
):
    announcement = await make_announcement()
    announcement_id = announcement.id
    assert (
        await management_service.preview_all_users(announcement_id)
    ).total_users == 4
    before_publish = User(email=f"before-{uuid4().hex}@example.com")
    db_session.add(before_publish)
    db_session.commit()

    await management_service.publish_to_all_users(announcement_id)
    published_at = announcement.published_at
    after_publish = User(email=f"after-{uuid4().hex}@example.com")
    db_session.add(after_publish)
    db_session.commit()

    with pytest.raises(ValueError, match="already published"):
        await management_service.publish_to_all_users(announcement_id)

    targets = await management_service.list_recipients(announcement_id)
    assert {target.user_id for target in targets} == {
        *[user.id for user in users],
        before_publish.id,
        admin.id,
    }
    assert await user_service.list_announcements_for_user(after_publish.id) == []
    assert (await management_service.get(announcement_id)).published_at == published_at


@pytest.mark.asyncio
async def test_all_users_without_existing_recipients(
    management_service, make_announcement
):
    announcement = await make_announcement()

    preview = await management_service.preview_all_users(announcement.id)

    assert preview.total_users == 1
    assert preview.existing_recipients == 0
    assert preview.new_recipients == 1
    assert preview.read_recipients == 0
    assert preview.unread_recipients == 0
    assert (await management_service.publish_to_all_users(announcement.id)).published
    assert len(await management_service.list_recipients(announcement.id)) == 1


@pytest.mark.asyncio
@pytest.mark.parametrize("method", ["preview_all_users", "publish_to_all_users"])
async def test_all_users_missing_announcement(management_service, method):
    with pytest.raises(LookupError, match="not found"):
        await getattr(management_service, method)(uuid4())


@pytest.mark.asyncio
async def test_publish_all_users_rolls_back_recipient_inserts(
    management_service, users, make_announcement, db_session, monkeypatch
):
    announcement = await make_announcement()
    announcement_id = announcement.id

    def fail_commit():
        # Verify recipient inserts happened before simulating a commit failure.
        from sqlmodel import select

        from backend.announcements.models import AnnouncementRecipient

        assert len(db_session.exec(select(AnnouncementRecipient)).all()) == 4
        raise RuntimeError("Commit failed")

    monkeypatch.setattr(db_session, "commit", fail_commit)
    with pytest.raises(RuntimeError, match="Commit failed"):
        await management_service.publish_to_all_users(announcement_id)

    stored = await management_service.get(announcement_id)
    assert not stored.published
    assert stored.published_at is None
    assert stored.audience_summary is None
    assert await management_service.list_recipients(announcement_id) == []


@pytest.mark.asyncio
async def test_creation_sets_owner_and_listing_is_scoped(
    management_service, make_user, admin, db_session
):
    from backend.announcements.models import AnnouncementRecipient

    other_admin = await make_user(role=UserRole.ADMIN)
    other_service = AnnouncementManagementService(db_session, other_admin)
    own = await management_service.create(
        Announcement(
            title="Own", message="Message", version="1", created_by_id=other_admin.id
        )
    )
    other = await other_service.create(
        Announcement(title="Other", message="Message", version="1")
    )
    assert own.created_by_id == admin.id
    assert [item.id for item in await management_service.list_all()] == [own.id]
    assert [item.id for item in await other_service.list_all()] == [other.id]
    assert not db_session.get(AnnouncementRecipient, (own.id, other_admin.id))


def test_management_service_rejects_non_admin(db_session, users):
    with pytest.raises(PermissionError, match="Admin access required"):
        AnnouncementManagementService(db_session, users[0])


@pytest.mark.asyncio
@pytest.mark.parametrize("ownerless", [False, True])
@pytest.mark.parametrize(
    "method",
    [
        "get",
        "update",
        "publish",
        "publish_to_all_users",
        "add_recipients",
        "remove_recipients",
        "list_recipients",
        "preview_all_users",
        "delete_announcement",
    ],
)
async def test_management_rejects_non_owned_announcements(
    management_service,
    users,
    make_announcement,
    db_session,
    method,
    ownerless,
    make_user,
):
    announcement = await make_announcement()
    announcement_id = announcement.id
    await management_service.add_recipients(announcement_id, [users[2].id])
    if ownerless:
        announcement.created_by_id = None
    db_session.commit()
    other_admin = await make_user(role=UserRole.ADMIN)
    intruder = AnnouncementManagementService(db_session, other_admin)
    arguments = [announcement_id]
    if method == "update":
        arguments.append(AnnoucementUpdate(title="Unauthorized"))
    elif method in {"add_recipients", "remove_recipients"}:
        arguments.append([users[2].id])

    with pytest.raises(LookupError, match="Announcement not found"):
        await getattr(intruder, method)(*arguments)

    db_session.expire_all()
    stored = await UserAnnouncementService(db_session).get(announcement_id)
    assert stored.title == "My First"
    assert not stored.published
    assert stored.published_at is None
    recipient = await UserAnnouncementService(db_session).retrieve_annoucement_for_user(
        users[2].id, announcement_id
    )
    assert recipient.read_at is None

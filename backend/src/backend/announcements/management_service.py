from collections.abc import Sequence
from datetime import UTC, datetime
from uuid import UUID

from sqlalchemy import delete, func, insert, literal
from sqlalchemy.sql.selectable import Exists
from sqlmodel import Session, col, select

from backend.accounts.models import Role, User, UserRole, UserRoleLink
from backend.announcements.models import (
    AnnoucementUpdate,
    Announcement,
    AnnouncementAudiencePreview,
    AnnouncementRecipient,
)
from backend.announcements.repository import AnnouncementRepository


def _matching_roles(roles: Sequence[UserRole] | None) -> Exists | None:
    if roles is None:
        return None
    if not roles:
        raise ValueError("Select at least one role, or omit roles to include all users")
    validated = [UserRole(role) for role in roles]
    return (
        select(UserRoleLink.user_id)
        .join(Role, col(Role.id) == col(UserRoleLink.role_id))
        .where(
            col(UserRoleLink.user_id) == col(User.id),
            col(Role.name).in_(validated),
        )
        .exists()
    )


def _audience_summary(roles: Sequence[UserRole] | None) -> str:
    if roles is None:
        return "All current users"
    labels = {
        UserRole.STUDENT: "students",
        UserRole.EDUCATOR: "educators",
        UserRole.ADMIN: "admins",
    }
    selected = [labels[role] for role in UserRole if role in roles]
    return "All current " + (
        selected[0]
        if len(selected) == 1
        else ", ".join(selected[:-1]) + " and " + selected[-1]
    )


class AnnouncementManagementService:
    def __init__(self, session: Session, actor: User) -> None:
        if not any(role.name == UserRole.ADMIN for role in actor.roles):
            raise PermissionError("Admin access required")
        self._actor_id = actor.id
        self._session = session
        self._repo = AnnouncementRepository(session)

    async def create(self, an: Announcement) -> Announcement:
        an.created_by_id = self._actor_id
        an = await self._repo.create(an)
        self._session.commit()
        return an

    async def list_all(self) -> Sequence[Announcement]:
        return self._session.exec(
            select(Announcement).where(Announcement.created_by_id == self._actor_id)
        ).all()

    async def get(self, an_id: UUID) -> Announcement:
        return await self._get_owned(an_id)

    async def _get_owned(
        self, announcement_id: UUID, *, for_update: bool = False
    ) -> Announcement:
        statement = select(Announcement).where(
            col(Announcement.id) == announcement_id,
            col(Announcement.created_by_id) == self._actor_id,
        )
        if for_update:
            statement = statement.with_for_update().execution_options(
                populate_existing=True
            )
        announcement = self._session.exec(statement).one_or_none()
        if announcement is None:
            raise LookupError("Announcement not found")
        return announcement

    async def publish_to_all_users(
        self, announcement_id: UUID, *, roles: Sequence[UserRole] | None = None
    ) -> Announcement:
        """Assign missing current users and publish atomically as an in-app snapshot."""
        try:
            # Serialize publication attempts for this announcement.
            announcement = await self._get_owned(announcement_id, for_update=True)
            if announcement.published:
                raise ValueError("Announcement is already published")
            role_filter = _matching_roles(roles)
            if self._count_conflicting_recipients(announcement_id, role_filter):
                raise ValueError(
                    "Existing recipients fall outside the selected roles. "
                    "Remove those recipients or select all users before publishing."
                )

            existing_recipient = (
                select(AnnouncementRecipient.user_id)
                .where(
                    col(AnnouncementRecipient.announcement_id) == announcement_id,
                    col(AnnouncementRecipient.user_id) == col(User.id),
                )
                .exists()
            )
            # Keep existing recipients and their read timestamps intact.
            recipients = select(literal(announcement_id), col(User.id)).where(
                ~existing_recipient
            )
            if role_filter is not None:
                recipients = recipients.where(role_filter)
            self._session.exec(
                insert(AnnouncementRecipient).from_select(
                    ["announcement_id", "user_id"], recipients
                )
            )
            announcement.published = True
            announcement.published_at = datetime.now(UTC)
            announcement.audience_summary = _audience_summary(roles)
            self._session.add(announcement)
            self._session.commit()
        except Exception:
            self._session.rollback()
            raise

        self._session.refresh(announcement)
        return announcement

    async def _assert_get(self, an_id: UUID) -> None:
        await self._get_owned(an_id)

    async def update(self, an_id: UUID, update: AnnoucementUpdate) -> Announcement:
        try:
            announcement = await self._get_owned(an_id, for_update=True)
            announcement = await self._repo.update(announcement, update)
            self._session.commit()
            return announcement
        except Exception:
            self._session.rollback()
            raise

    async def add_recipients(
        self, announcement_id: UUID, users_id: Sequence[UUID]
    ) -> Sequence[AnnouncementRecipient]:
        try:
            await self._get_owned(announcement_id, for_update=True)
            # Checks existing
            existing_recipients = (
                select(AnnouncementRecipient.user_id)
                .where(
                    col(AnnouncementRecipient.announcement_id) == announcement_id,
                    col(AnnouncementRecipient.user_id) == col(User.id),
                )
                .exists()
            )
            recipients = select(literal(announcement_id), col(User.id)).where(
                col(User.id).in_(users_id), ~existing_recipients
            )
            result = self._session.exec(
                insert(AnnouncementRecipient)
                .from_select(["announcement_id", "user_id"], recipients)
                .returning(AnnouncementRecipient)
            )
            targets = result.scalars().all()
            self._session.commit()
            self._session.flush()
        except Exception:
            self._session.rollback()
            raise

        return targets

    async def remove_recipients(self, an_id: UUID, user_ids: Sequence[UUID]) -> None:
        try:
            await self._get_owned(an_id, for_update=True)
            self._session.exec(
                delete(AnnouncementRecipient).where(
                    col(AnnouncementRecipient.announcement_id) == an_id,
                    col(AnnouncementRecipient.user_id).in_(user_ids),
                )
            )
            self._session.commit()
        except Exception:
            self._session.rollback()
            raise

    async def list_recipients(self, an_id: UUID) -> Sequence[AnnouncementRecipient]:
        try:
            await self._assert_get(an_id)
            return self._session.exec(
                select(AnnouncementRecipient).where(
                    col(AnnouncementRecipient.announcement_id) == an_id
                )
            ).all()
        except Exception:
            self._session.rollback()
            raise

    async def publish(self, an_id: UUID) -> Announcement:
        try:
            announcement = await self._get_owned(an_id, for_update=True)
            if not announcement.published:
                announcement.published = True
                announcement.published_at = datetime.now(UTC)
            self._session.add(announcement)
            self._session.commit()
        except Exception:
            self._session.rollback()
            raise
        self._session.refresh(announcement)
        return announcement

    async def delete_announcement(self, an_id: UUID) -> None:
        try:
            await self._get_owned(an_id, for_update=True)
            self._session.execute(
                delete(AnnouncementRecipient).where(
                    col(AnnouncementRecipient.announcement_id) == an_id
                )
            )
            await self._repo.delete(an_id)
            self._session.commit()
        except Exception:
            self._session.rollback()
            raise

    async def preview_all_users(
        self, announcement_id: UUID, *, roles: Sequence[UserRole] | None = None
    ) -> AnnouncementAudiencePreview:
        """Count the current audience without assigning recipients or publishing."""
        announcement = await self._get_owned(announcement_id)
        role_filter = _matching_roles(roles)

        statement = (
            select(
                func.count(col(User.id)),
                func.count(col(AnnouncementRecipient.user_id)),
                func.count(col(AnnouncementRecipient.read_at)),
            )
            .select_from(User)
            .outerjoin(
                AnnouncementRecipient,
                (col(AnnouncementRecipient.user_id) == col(User.id))
                & (col(AnnouncementRecipient.announcement_id) == announcement_id),
            )
        )
        if role_filter is not None:
            statement = statement.where(role_filter)
        total, existing, read = self._session.exec(statement).one()
        return AnnouncementAudiencePreview(
            announcement_id=announcement_id,
            published=announcement.published,
            total_users=total,
            existing_recipients=existing,
            new_recipients=total - existing,
            read_recipients=read,
            unread_recipients=existing - read,
            conflicting_recipients=self._count_conflicting_recipients(
                announcement_id, role_filter
            ),
        )

    def _count_conflicting_recipients(
        self, announcement_id: UUID, role_filter: Exists | None
    ) -> int:
        if role_filter is None:
            return 0
        return self._session.exec(
            select(func.count())
            .select_from(User)
            .join(
                AnnouncementRecipient,
                col(AnnouncementRecipient.user_id) == col(User.id),
            )
            .where(
                col(AnnouncementRecipient.announcement_id) == announcement_id,
                ~role_filter,
            )
        ).one()

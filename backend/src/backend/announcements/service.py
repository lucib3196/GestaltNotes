from collections.abc import Sequence
from datetime import UTC, datetime
from uuid import UUID

from sqlalchemy import delete
from sqlmodel import Session, col, select

from backend.adapters.repository import Repository
from backend.announcements.models import (
    AnnoucementUpdate,
    Announcement,
    AnnouncementRecipient,
)


class AnnoucementRepo(Repository[Announcement, AnnoucementUpdate]):
    def __init__(
        self,
        session: Session,
    ) -> None:
        super().__init__(session, Announcement)


class AnnoucementService:
    def __init__(self, session: Session) -> None:
        self._session = session
        self._repo = AnnoucementRepo(session)

    async def create(self, an: Announcement) -> Announcement:
        an = await self._repo.create(an)
        self._session.commit()
        return an

    async def get(self, an_id: UUID) -> Announcement | None:
        return await self._repo.get(an_id)

    async def _assert_get(self, an_id: UUID) -> None:
        an = await self._repo.get(an_id)
        if not an:
            raise ValueError("Cannot retrieve annoucement. Annoucement does not exist")

    async def update(self, an_id: UUID, update: AnnoucementUpdate) -> Announcement:
        announcement = await self._repo.update_by_id(an_id, update)
        self._session.commit()
        return announcement

    async def add_recipients(
        self, an_id: UUID, users_id: Sequence[UUID]
    ) -> Sequence[AnnouncementRecipient]:
        with self._session.begin():
            announcement = await self._repo.get(an_id)
            if announcement is None:
                raise ValueError(
                    "Cannot attach recipients. Cannot determine announcement"
                )

            targets = [
                AnnouncementRecipient(
                    announcement_id=announcement.id,
                    user_id=uid,
                )
                for uid in users_id
            ]
            self._session.add_all(targets)
            self._session.flush(targets)

        return targets

    async def remove_recipients(self, an_id: UUID, user_ids: Sequence[UUID]) -> None:
        try:
            await self._assert_get(an_id)
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
            announcement = await self._repo.get(an_id)
            if announcement is None:
                raise ValueError("Announcement does not exist")
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

    async def list_announcements_for_user(
        self, user_id: UUID
    ) -> Sequence[Announcement]:
        stmt = (
            select(Announcement)
            .join(
                AnnouncementRecipient,
                col(AnnouncementRecipient.announcement_id) == col(Announcement.id),
            )
            .where(
                col(AnnouncementRecipient.user_id) == user_id,
                col(Announcement.published).is_(True),
            )
            .order_by(col(Announcement.published_at).desc())
        )
        return self._session.exec(stmt).all()

    async def retrieve_annoucement_for_user(
        self, user_id: UUID, an_id: UUID
    ) -> AnnouncementRecipient:
        stmt = (
            select(AnnouncementRecipient)
            .where(AnnouncementRecipient.user_id == user_id)
            .where(AnnouncementRecipient.announcement_id == an_id)
        )
        an = self._session.exec(stmt).first()
        if not an:
            raise ValueError(
                f"Failed to retrieve annoucement data. It does not exist with {an_id}"
            )
        return an

    async def mark_announcement_read(
        self, user_id: UUID, an_id: UUID
    ) -> AnnouncementRecipient:
        recipient = await self.retrieve_annoucement_for_user(user_id, an_id)
        if recipient.read_at is None:
            # The current read_at column stores timestamps without timezone.
            recipient.read_at = datetime.now(UTC).replace(tzinfo=None)
        try:
            self._session.add(recipient)
            self._session.commit()
        except Exception:
            self._session.rollback()
            raise
        self._session.refresh(recipient)
        return recipient

    async def delete_announcement(self, an_id: UUID) -> None:
        try:
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

from collections.abc import Sequence
from datetime import UTC, datetime
from uuid import UUID

from sqlmodel import Session, col, select

from backend.announcements.models import Announcement, AnnouncementRecipient
from backend.announcements.repository import AnnouncementRepository


class UserAnnouncementService:
    def __init__(self, session: Session) -> None:
        self._session = session
        self._repo = AnnouncementRepository(session)

    async def get(self, an_id: UUID) -> Announcement | None:
        return await self._repo.get(an_id)

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

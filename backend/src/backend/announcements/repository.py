from sqlmodel import Session

from backend.adapters.repository import Repository
from backend.announcements.models import AnnoucementUpdate, Announcement


class AnnouncementRepository(Repository[Announcement, AnnoucementUpdate]):
    def __init__(self, session: Session) -> None:
        super().__init__(session, Announcement)

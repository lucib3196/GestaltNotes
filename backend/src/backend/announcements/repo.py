from typing import Any

from backend.adapters.repository import Repository
from backend.announcements.models import AnnouncementBase, Announcement
from sqlmodel import Session


class AnnouncementRepo(Repository[AnnouncementBase, Announcement]):
    def __init__(self, session: Session):
        self._session = session
        
        
    def create(self, record: AnnouncementBase) -> AnnouncementBase:
        return super().create(record)

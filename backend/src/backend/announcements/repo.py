from sqlmodel import Session

from backend.adapters.repository import Repository
from backend.announcements.models import AnnoucementUpdate, Announcement


class AnnoucementRepo(Repository[Announcement, AnnoucementUpdate]):
    def __init__(self, session: Session, model: type[Announcement]) -> None:
        super().__init__(session, model)

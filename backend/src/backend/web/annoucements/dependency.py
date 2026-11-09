from typing import Annotated

from fastapi import Depends

from backend.announcements.management_service import AnnouncementManagementService
from backend.announcements.user_service import UserAnnouncementService
from backend.database import SessionDep
from backend.web.accounts.dependencies import AdminDep


def get_announcement_management_service(
    session: SessionDep,
    admin: AdminDep,
) -> AnnouncementManagementService:
    return AnnouncementManagementService(session, admin)


def get_user_announcement_service(session: SessionDep) -> UserAnnouncementService:
    return UserAnnouncementService(session)


AnnouncementManagementDep = Annotated[
    AnnouncementManagementService, Depends(get_announcement_management_service)
]
UserAnnouncementDep = Annotated[
    UserAnnouncementService, Depends(get_user_announcement_service)
]

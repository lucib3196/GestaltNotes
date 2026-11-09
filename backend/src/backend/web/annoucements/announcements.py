from collections.abc import Sequence
from uuid import UUID

from fastapi import APIRouter, HTTPException

from backend.announcements.models import Announcement, AnnouncementRecipient
from backend.web.accounts.dependencies import CurrentUserDep

from .dependency import UserAnnouncementDep

router = APIRouter(tags=["announcements"], prefix="/announcements")


@router.get("/", response_model=list[Announcement])
async def list_my_announcements(
    service: UserAnnouncementDep,
    user: CurrentUserDep,
) -> Sequence[Announcement]:
    return await service.list_announcements_for_user(user.id)


@router.get("/{announcement_id}", response_model=Announcement)
async def get_my_announcement(
    announcement_id: UUID,
    service: UserAnnouncementDep,
    user: CurrentUserDep,
) -> Announcement:
    announcement = await service.get(announcement_id)
    if announcement is None or not announcement.published:
        raise HTTPException(status_code=404, detail="Announcement not found")
    try:
        await service.retrieve_annoucement_for_user(user.id, announcement_id)
    except ValueError as exc:
        raise HTTPException(status_code=404, detail="Announcement not found") from exc
    return announcement


@router.put("/{announcement_id}/read", response_model=AnnouncementRecipient)
async def mark_announcement_read(
    announcement_id: UUID,
    service: UserAnnouncementDep,
    user: CurrentUserDep,
) -> AnnouncementRecipient:
    announcement = await service.get(announcement_id)
    if announcement is None or not announcement.published:
        raise HTTPException(status_code=404, detail="Announcement not found")
    try:
        return await service.mark_announcement_read(user.id, announcement_id)
    except ValueError as exc:
        raise HTTPException(status_code=404, detail="Announcement not found") from exc

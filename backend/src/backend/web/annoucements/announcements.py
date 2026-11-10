from collections.abc import Sequence
from uuid import UUID

from fastapi import APIRouter, HTTPException, Query

from backend.announcements.models import (
    Announcement,
    AnnouncementHistoryPage,
    AnnouncementRecipient,
)
from backend.web.accounts.dependencies import CurrentUserDep

from .dependency import UserAnnouncementDep

router = APIRouter(tags=["announcements"], prefix="/announcements")


@router.get("/", response_model=list[Announcement])
async def list_my_announcements(
    service: UserAnnouncementDep,
    user: CurrentUserDep,
    unread_only: bool = False,
) -> Sequence[Announcement]:
    return await service.list_announcements_for_user(user.id, unread_only=unread_only)


@router.get("/history", response_model=AnnouncementHistoryPage)
async def list_announcement_history(
    service: UserAnnouncementDep,
    user: CurrentUserDep,
    limit: int = Query(default=5, ge=1, le=5),
    offset: int = Query(default=0, ge=0),
) -> AnnouncementHistoryPage:
    return await service.list_announcement_history(user.id, limit=limit, offset=offset)


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

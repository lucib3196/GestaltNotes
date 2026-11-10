from collections.abc import Sequence
from typing import Annotated
from uuid import UUID

from fastapi import APIRouter, HTTPException, Query, status
from pydantic import BaseModel
from sqlalchemy.exc import IntegrityError

from backend.accounts.models import UserRole
from backend.announcements.models import (
    AnnoucementUpdate,
    Announcement,
    AnnouncementAudiencePreview,
    AnnouncementBase,
    AnnouncementRecipient,
)

from .dependency import AnnouncementManagementDep

router = APIRouter(tags=["announcement management"], prefix="/admin/announcements")


class RecipientRequest(BaseModel):
    user_ids: list[UUID]


###############################################################################
### Announcement management
###############################################################################


@router.get("/")
async def get_all(
    service: AnnouncementManagementDep,
) -> Sequence[Announcement]:
    return await service.list_all()


@router.post("/", response_model=Announcement, status_code=status.HTTP_201_CREATED)
async def create_announcement(
    data: AnnouncementBase,
    service: AnnouncementManagementDep,
) -> Announcement:
    if data.published:
        raise HTTPException(
            status_code=422,
            detail="Create a draft, then use the publish endpoint",
        )
    return await service.create(Announcement.model_validate(data))


@router.get("/{announcement_id}", response_model=Announcement)
async def get_announcement(
    announcement_id: UUID,
    service: AnnouncementManagementDep,
) -> Announcement:
    try:
        return await service.get(announcement_id)
    except LookupError as exc:
        raise HTTPException(status_code=404, detail="Announcement not found") from exc


@router.patch("/{announcement_id}", response_model=Announcement)
async def update_announcement(
    announcement_id: UUID,
    data: AnnoucementUpdate,
    service: AnnouncementManagementDep,
) -> Announcement:
    changes = data.model_dump(exclude_unset=True)
    if "published" in changes:
        raise HTTPException(
            status_code=422,
            detail="Use the publish endpoint to publish an announcement",
        )
    if any(value is None for value in changes.values()):
        raise HTTPException(
            status_code=422, detail="Announcement fields cannot be null"
        )
    try:
        return await service.update(announcement_id, data)
    except LookupError as exc:
        raise HTTPException(status_code=404, detail="Announcement not found") from exc


@router.post("/{announcement_id}/publish", response_model=Announcement)
async def publish_announcement(
    announcement_id: UUID,
    service: AnnouncementManagementDep,
) -> Announcement:
    try:
        return await service.publish(announcement_id)
    except LookupError as exc:
        raise HTTPException(status_code=404, detail="Announcement not found") from exc


@router.delete("/{announcement_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_announcement(
    announcement_id: UUID,
    service: AnnouncementManagementDep,
) -> None:
    try:
        await service.delete_announcement(announcement_id)
    except LookupError as exc:
        raise HTTPException(status_code=404, detail="Announcement not found") from exc


@router.get(
    "/{announcement_id}/audience-preview",
    response_model=AnnouncementAudiencePreview,
)
async def preview_all_users(
    announcement_id: UUID,
    service: AnnouncementManagementDep,
    roles: Annotated[list[UserRole] | None, Query()] = None,
) -> AnnouncementAudiencePreview:
    try:
        return await service.preview_all_users(announcement_id, roles=roles)
    except LookupError as exc:
        raise HTTPException(status_code=404, detail="Announcement not found") from exc


@router.post("/{announcement_id}/publish-to-all", response_model=Announcement)
async def publish_to_all_users(
    announcement_id: UUID,
    service: AnnouncementManagementDep,
    roles: Annotated[list[UserRole] | None, Query()] = None,
) -> Announcement:
    try:
        return await service.publish_to_all_users(announcement_id, roles=roles)
    except LookupError as exc:
        raise HTTPException(status_code=404, detail="Announcement not found") from exc
    except ValueError as exc:
        raise HTTPException(status_code=409, detail=str(exc)) from exc


###############################################################################
### Recipient management
###############################################################################


@router.get("/{announcement_id}/recipients", response_model=list[AnnouncementRecipient])
async def list_recipients(
    announcement_id: UUID,
    service: AnnouncementManagementDep,
) -> Sequence[AnnouncementRecipient]:
    try:
        return await service.list_recipients(announcement_id)
    except LookupError as exc:
        raise HTTPException(status_code=404, detail="Announcement not found") from exc


@router.post(
    "/{announcement_id}/recipients",
    response_model=list[AnnouncementRecipient],
    status_code=status.HTTP_201_CREATED,
)
async def add_recipients(
    announcement_id: UUID,
    data: RecipientRequest,
    service: AnnouncementManagementDep,
) -> Sequence[AnnouncementRecipient]:
    try:
        return await service.add_recipients(announcement_id, data.user_ids)
    except LookupError as exc:
        raise HTTPException(status_code=404, detail="Announcement not found") from exc
    except IntegrityError as exc:
        raise HTTPException(
            status_code=409,
            detail="Recipients already exist or reference users that do not exist",
        ) from exc


@router.delete("/{announcement_id}/recipients", status_code=status.HTTP_204_NO_CONTENT)
async def remove_recipients(
    announcement_id: UUID,
    data: RecipientRequest,
    service: AnnouncementManagementDep,
) -> None:
    try:
        await service.remove_recipients(announcement_id, data.user_ids)
    except LookupError as exc:
        raise HTTPException(status_code=404, detail="Announcement not found") from exc

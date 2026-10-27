from urllib.parse import quote
from uuid import UUID

from fastapi import HTTPException
from fastapi.responses import Response
from fastapi.routing import APIRouter
from starlette import status

from backend.storage.exceptions import (
    FileNotFoundError,
    FileServiceRetrievalError,
)
from backend.web.accounts.dependencies import CurrentUserDep

from .dependency import FileServiceDep

router = APIRouter(prefix="/files", tags=["files"])


@router.get("")
async def get_file(
    service: FileServiceDep,
    _user: CurrentUserDep,
    file_id: UUID | None = None,
    storage_key: str | None = None,
) -> Response:
    if (file_id is None) == (storage_key is None):
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="Provide exactly one of file_id or storage_key",
        )

    try:
        file, data = await service.download_file(file_id, storage_key=storage_key)
    except FileNotFoundError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="File not found",
        ) from e
    except FileServiceRetrievalError as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to retrieve file",
        ) from e

    return Response(
        content=data,
        media_type=file.content_type or "application/octet-stream",
        headers={
            "Content-Disposition": (
                f"inline; filename*=UTF-8''{quote(file.original_name, safe='')}"
            ),
        },
    )


@router.get("/{file_id}")
async def get_file_by_id(
    file_id: UUID,
    service: FileServiceDep,
    _user: CurrentUserDep,
) -> Response:
    return await get_file(
        service=service,
        _user=_user,
        file_id=file_id,
    )

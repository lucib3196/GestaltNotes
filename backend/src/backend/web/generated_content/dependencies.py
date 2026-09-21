from typing import Annotated

from fastapi import Depends, HTTPException
from starlette import status

from backend.core import logger
from backend.service.generated_content import GeneratedMCQService
from backend.web.dependencies import SessionDep


def get_mcq_service(session: SessionDep) -> GeneratedMCQService:
    """Create a UserManager scoped to the current request session."""
    try:
        return GeneratedMCQService(session)
    except Exception as e:
        logger.exception("Failed to initialize UserManager")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to initialize user service",
        ) from e


GenMCQDependency = Annotated[GeneratedMCQService, Depends(get_mcq_service)]

from src.service.generated_content import GeneratedMCQService
from src.web.dependencies import SessionDep
from typing import Annotated
from fastapi import HTTPException, Depends
from starlette import status
from src.core import logger


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

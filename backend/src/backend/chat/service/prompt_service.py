from collections.abc import Sequence
from typing import Literal
from uuid import UUID

from authorization import AccessDecision, OwnershipAccessGate
from pydantic import BaseModel, Field
from sqlalchemy import Select
from sqlalchemy.exc import SQLAlchemyError
from sqlmodel import Session, col, select

from backend.accounts.models import User, UserRole
from backend.chat.exceptions import PromptNotFoundError, PromptServiceError
from backend.chat.model import Prompt, PromptBase, PromptSummary, PromptUpdate
from backend.chat.repo.prompt_repo import PromptRepo
from backend.core.logger import logger


class PromptAccessGate(OwnershipAccessGate[UserRole, Prompt, User]):
    def get_roles(self, actor: User) -> list[UserRole]:
        return [role.name for role in actor.roles]

    def check_access(self, actor: User, resource: Prompt) -> AccessDecision:
        access = resource.user_id == actor.id
        return AccessDecision(
            access=access, message=f"User has access to prompt {access}"
        )

    def check_ownership(self, actor: User, resource: Prompt) -> AccessDecision:
        return self.check_access(actor, resource)


class PaginationOptions(BaseModel):
    offset: int = Field(default=0, ge=0)
    limit: int = Field(default=20, ge=1, le=100)
    sort: Literal["updated", "created"] = "updated"
    order: Literal["desc", "asc"] = "desc"


class PromptService:
    name = "PromptService"

    def __init__(self, session: Session, access: PromptAccessGate) -> None:
        self._session = session
        self._prompts = PromptRepo(session)
        self._access = access

    async def create(self, data: PromptBase, user: User) -> Prompt:
        try:
            prompt = await self._prompts.create(
                Prompt(
                    title=data.title,
                    description=data.description,
                    content=data.content,
                    user_id=user.id,
                )
            )
            self._session.commit()
            return prompt
        except SQLAlchemyError as exc:
            self._session.rollback()
            logger.exception("Failed to create prompt")
            raise PromptServiceError("Failed to create prompt") from exc

    async def get_prompt_by_id(self, uid: UUID, user: User) -> Prompt:
        try:
            prompt = await self._prompts.get(uid)
        except SQLAlchemyError as exc:
            self._session.rollback()
            logger.exception("Failed to retrieve prompt")
            raise PromptServiceError("Failed to retrieve prompt") from exc
        if prompt is None:
            raise PromptNotFoundError(f"Prompt {uid} does not exist")

        self._access.require_access(user, prompt)
        return prompt

    async def update_prompt(
        self, uid: UUID, update: PromptUpdate, user: User
    ) -> Prompt:
        prompt = await self.get_prompt_by_id(uid, user)
        try:
            prompt = await self._prompts.update(record=prompt, update=update)
            self._session.commit()
            return prompt
        except SQLAlchemyError as exc:
            self._session.rollback()
            logger.exception("Failed to update prompt")
            raise PromptServiceError("Failed to update prompt") from exc

    async def delete_prompt(self, uid: UUID, user: User) -> bool:
        prompt = await self.get_prompt_by_id(uid, user)
        try:
            await self._prompts.delete(prompt.id)
            self._session.commit()
            return True
        except SQLAlchemyError as exc:
            self._session.rollback()
            logger.exception("Failed to delete prompt")
            raise PromptServiceError("Failed to delete prompt") from exc

    async def list_user_prompts(
        self, user: User, options: PaginationOptions | None = None
    ) -> Sequence[Prompt]:
        stmt = select(Prompt).where(Prompt.user_id == user.id)
        stmt = self._format_pagination(stmt, options or PaginationOptions())
        try:
            return self._session.exec(stmt).all()
        except SQLAlchemyError as exc:
            self._session.rollback()
            logger.exception("Failed to list prompts")
            raise PromptServiceError("Failed to list prompts") from exc

    async def list_user_prompts_by_title(
        self, user: User, options: PaginationOptions | None = None
    ) -> Sequence[PromptSummary]:
        stmt = select(Prompt.id, Prompt.title, Prompt.description).where(
            Prompt.user_id == user.id
        )
        stmt = self._format_pagination(stmt, options or PaginationOptions())
        try:
            return [
                PromptSummary(id=uid, title=title, description=description)
                for uid, title, description in self._session.exec(stmt).all()
            ]
        except SQLAlchemyError as exc:
            self._session.rollback()
            logger.exception("Failed to list prompts")
            raise PromptServiceError("Failed to list prompts") from exc

    def _format_pagination(self, stmt: Select, options: PaginationOptions) -> Select:
        sort_column = (
            col(Prompt.updated_at)
            if options.sort == "updated"
            else col(Prompt.created_at)
        )
        sort_order = (
            sort_column.desc() if options.order == "desc" else sort_column.asc()
        )
        return (
            stmt.order_by(sort_order, col(Prompt.id).asc())
            .offset(options.offset)
            .limit(options.limit)
        )

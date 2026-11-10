from abc import ABC, abstractmethod
from typing import Generic, Protocol, TypeVar
from uuid import UUID

from pydantic import BaseModel

from authorization.exceptions import AccessDeniedError, RoleAccessDeniedError

RoleT = TypeVar("RoleT", bound=str)
ResourceT = TypeVar("ResourceT", bound=BaseModel)


class Actor(Protocol[RoleT]):
    id: UUID
    roles: list[RoleT]


class AccessDecision(BaseModel):
    """The outcome of an authorization check."""

    access: bool
    message: str | None = None


class AccessGate(Generic[RoleT, ResourceT], ABC):
    """Check and enforce access rules for actors and resources."""

    @abstractmethod
    def check_access(self, actor: Actor[RoleT], resource: ResourceT) -> AccessDecision:
        """Return whether the actor may access the resource."""
        ...

    def check_roles(
        self, actor: Actor[RoleT], allowed_roles: list[RoleT]
    ) -> AccessDecision:
        """Allow any matching role; deny when allowed roles are empty."""
        return AccessDecision(access=any(role in allowed_roles for role in actor.roles))

    def require_roles(
        self, actor: Actor[RoleT], allowed_roles: list[RoleT]
    ) -> AccessDecision:
        """Raise RoleAccessDeniedError unless an allowed role matches."""
        decision = self.check_roles(actor, allowed_roles)
        if not decision.access:
            raise RoleAccessDeniedError(list(allowed_roles))
        return decision

    def require_access(
        self, actor: Actor[RoleT], resource: ResourceT
    ) -> AccessDecision:
        """Raise AccessDeniedError unless resource access is allowed."""
        decision = self.check_access(actor, resource)
        if not decision.access:
            raise AccessDeniedError(decision.message or "Access denied")
        return decision


class OwnershipAccessGate(AccessGate[RoleT, ResourceT], ABC):
    """Check and enforce access to resources with ownership."""

    @abstractmethod
    def check_ownership(
        self, actor: Actor[RoleT], resource: ResourceT
    ) -> AccessDecision:
        """Return whether the actor owns the resource."""
        ...

    def require_ownership(
        self, actor: Actor[RoleT], resource: ResourceT
    ) -> AccessDecision:
        """Raise AccessDeniedError unless the actor owns the resource."""
        decision = self.check_ownership(actor, resource)
        if not decision.access:
            raise AccessDeniedError(decision.message or "Resource ownership required")
        return decision

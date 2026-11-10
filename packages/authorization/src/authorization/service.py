from abc import ABC, abstractmethod
from collections.abc import Iterable
from typing import Generic, Protocol, TypeVar
from uuid import UUID

from pydantic import BaseModel

from authorization.exceptions import AccessDeniedError, RoleAccessDeniedError

RoleT = TypeVar("RoleT", bound=str)
ResourceT = TypeVar("ResourceT", bound=BaseModel)


class Actor(Protocol):
    id: UUID


ActorT = TypeVar("ActorT", bound=Actor)


class AccessDecision(BaseModel):
    """The outcome of an authorization check."""

    access: bool
    message: str | None = None


class AccessGate(ABC, Generic[RoleT, ResourceT, ActorT]):
    """Check and enforce access rules for actors and resources."""

    @abstractmethod
    def check_access(self, actor: ActorT, resource: ResourceT) -> AccessDecision:
        """Return whether the actor may access the resource."""
        ...

    @abstractmethod
    def get_roles(self, actor: ActorT) -> Iterable[RoleT]:
        """Return the actor's authorization roles."""
        ...

    def check_roles(self, actor: ActorT, allowed_roles: list[RoleT]) -> AccessDecision:
        return AccessDecision(
            access=any(role in allowed_roles for role in self.get_roles(actor))
        )

    def require_roles(
        self, actor: ActorT, allowed_roles: list[RoleT]
    ) -> AccessDecision:
        """Raise RoleAccessDeniedError unless an allowed role matches."""
        decision = self.check_roles(actor, allowed_roles)
        if not decision.access:
            raise RoleAccessDeniedError(list(allowed_roles))
        return decision

    def require_access(self, actor: ActorT, resource: ResourceT) -> AccessDecision:
        """Raise AccessDeniedError unless resource access is allowed."""
        decision = self.check_access(actor, resource)
        if not decision.access:
            raise AccessDeniedError(decision.message or "Access denied")
        return decision


class OwnershipAccessGate(AccessGate[RoleT, ResourceT, ActorT], ABC):
    """Check and enforce access to resources with ownership."""

    @abstractmethod
    def check_ownership(self, actor: ActorT, resource: ResourceT) -> AccessDecision:
        """Return whether the actor owns the resource."""
        ...

    def require_ownership(self, actor: ActorT, resource: ResourceT) -> AccessDecision:
        """Raise AccessDeniedError unless the actor owns the resource."""
        decision = self.check_ownership(actor, resource)
        if not decision.access:
            raise AccessDeniedError(decision.message or "Resource ownership required")
        return decision

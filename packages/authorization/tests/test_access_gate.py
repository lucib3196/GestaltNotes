from enum import StrEnum
from uuid import UUID, uuid4

import pytest
from pydantic import BaseModel

from authorization import (
    AccessDecision,
    AccessDeniedError,
    Actor,
    OwnershipAccessGate,
    RoleAccessDeniedError,
)


class Role(StrEnum):
    MEMBER = "member"
    ADMIN = "admin"


class User(BaseModel):
    id: UUID
    roles: list[Role]


class Resource(BaseModel):
    owner_id: UUID


class ResourceGate(OwnershipAccessGate[Role, Resource]):
    def check_access(self, actor: Actor[Role], resource: Resource) -> AccessDecision:
        return self.check_ownership(actor, resource)

    def check_ownership(self, actor: Actor[Role], resource: Resource) -> AccessDecision:
        return AccessDecision(access=actor.id == resource.owner_id)


def test_owner_has_access():
    user = User(id=uuid4(), roles=[Role.MEMBER])
    resource = Resource(owner_id=user.id)
    gate = ResourceGate()

    assert gate.require_access(user, resource).access
    assert gate.require_ownership(user, resource).access


def test_non_owner_is_denied():
    user = User(id=uuid4(), roles=[Role.MEMBER])
    resource = Resource(owner_id=uuid4())
    gate = ResourceGate()

    assert not gate.check_access(user, resource).access

    with pytest.raises(AccessDeniedError):
        gate.require_access(user, resource)

    with pytest.raises(AccessDeniedError):
        gate.require_ownership(user, resource)


def test_role_requirements():
    user = User(id=uuid4(), roles=[Role.MEMBER])
    gate = ResourceGate()

    assert gate.require_roles(user, [Role.MEMBER]).access

    with pytest.raises(RoleAccessDeniedError):
        gate.require_roles(user, [Role.ADMIN])

    assert not gate.check_roles(user, []).access

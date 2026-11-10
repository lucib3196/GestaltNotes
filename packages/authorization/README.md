# Authorization

Reusable policies for role checks, resource access, and ownership. Define application policies in the consuming app and keep shared behavior tests in this package.

- `AccessGate`: implement `check_access()` for your resource policy.
- `OwnershipAccessGate`: also implement `check_ownership()` when ownership applies.
- `check_*` methods return an `AccessDecision`, including denials.
- `require_*` methods return an allowed decision or raise `AccessDeniedError` (`RoleAccessDeniedError` for role denials).
- Role checks accept any matching role; an empty allowed list denies access.

## Example

```python
from enum import StrEnum
from uuid import UUID, uuid4

from pydantic import BaseModel
from authorization import AccessDecision, Actor, OwnershipAccessGate


class Role(StrEnum):
    MEMBER = "member"


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


user = User(id=uuid4(), roles=[Role.MEMBER])
resource = Resource(owner_id=user.id)
gate = ResourceGate()
gate.require_roles(user, [Role.MEMBER])
gate.require_access(user, resource)
```

Actors expose a UUID `id` and a list of role values. Adapt database role objects to enum values before passing them to a gate. Resources currently use Pydantic models. Ownership is one possible access rule; applications decide whether other roles may also grant access.

## Run tests

From `packages/authorization`:

```sh
uv run --locked pytest -q
```

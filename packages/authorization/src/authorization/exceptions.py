class AccessDeniedError(PermissionError):
    """An actor is not permitted to perform an action."""

    def __init__(self, message: str = "Access denied") -> None:
        super().__init__(message)


class RoleAccessDeniedError(AccessDeniedError):
    """An actor has none of the roles required for an action."""

    def __init__(self, allowed_roles: list[str]) -> None:
        self.allowed_roles = tuple(allowed_roles)
        super().__init__("Access requires at least one allowed role")

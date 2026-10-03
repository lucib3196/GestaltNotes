class DatabaseConfigError(Exception):
    """Raised when database configuration is invalid for the current environment."""


class DatabaseInitializationError(Exception):
    """Raised when creating the database engine/session setup fails."""


class DatabaseSessionError(Exception):
    """Raised for unexpected database session lifecycle failures."""

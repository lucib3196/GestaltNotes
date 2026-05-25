"""Core application exceptions for config, database, and firebase flows."""


class GestaltCoreError(Exception):
    """Base exception for core-level failures."""


# Config exceptions
class ConfigError(GestaltCoreError):
    """Base exception for application configuration issues."""


class MissingConfigError(ConfigError):
    """Raised when a required config value is missing."""


class InvalidConfigError(ConfigError):
    """Raised when a config value is present but invalid."""


class CredentialConfigError(ConfigError):
    """Raised when credential config is malformed or unreadable."""


class EmulatorConfigError(ConfigError):
    """Raised when emulator config is required but missing/invalid."""


# Database exceptions
class DatabaseConfigError(GestaltCoreError):
    """Raised when database configuration is invalid for the current environment."""


class DatabaseInitializationError(GestaltCoreError):
    """Raised when creating the database engine/session setup fails."""


class DatabaseSessionError(GestaltCoreError):
    """Raised for unexpected database session lifecycle failures."""


# Firebase exceptions
class FirebaseError(GestaltCoreError):
    """Base exception for Firebase-related failures."""


class FirebaseConfigError(FirebaseError):
    """Raised when Firebase config values are missing or invalid."""


class FirebaseInitializationError(FirebaseError):
    """Raised when Firebase app initialization fails."""


class FirebaseCredentialError(FirebaseError):
    """Raised when Firebase credentials cannot be loaded/validated."""


# Langchain Erroors
class LangchainError(GestaltCoreError):
    """Base exception for LangchainError-related failures."""


class MissingLangchainAPIKey(LangchainError):
    """raise when api key is missing"""


class MissingStreamURl(LangchainError):
    """raise when stream url is none"""

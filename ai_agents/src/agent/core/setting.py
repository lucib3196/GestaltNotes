from __future__ import annotations

from functools import lru_cache
from pathlib import Path
from typing import Literal

from dotenv import load_dotenv
from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict

# Load .env variables before settings are instantiated.


ROOT_PATH = Path(__file__).parents[3]
ENV = Literal["dev", "production"]

ENV_FILES: dict[str, str] = {
    "dev": ".env.dev",
    "test": ".env.testing",
    "testing": ".env.testing",
    "docker": ".env.docker",
}
env_file = ROOT_PATH / ENV_FILES.get(ENV, ".env.dev")  # type: ignore
load_dotenv(env_file, override=False)


class Settings(BaseSettings):
    """Application settings loaded from environment variables."""

    # AI model configuration
    model: str = "gemini-2.5-flash"
    embedding_model: str = "gemini-embedding-001"
    mode: ENV = Field(alias="ENV", default="dev")
    prompt_source: Literal["local", "production"] | None = None

    # External service keys
    GOOGLE_API_KEY: str | None = None
    LANGSMITH_API_KEY: str | None = None
    LANGSMITH_PROJECT: str | None = None

    # Vectordatabase
    ASTRA_DB_API_ENDPOINT: str | None = None
    ASTRA_DB_APPLICATION_TOKEN: str | None = None

    DATABASE_URL: str | None = None

    model_config = SettingsConfigDict(
        env_file=env_file,
        extra="ignore",
    )


@lru_cache
def get_settings() -> Settings:
    """Return cached validated application settings."""
    if not Settings().model:  # type: ignore
        raise ValueError("Failed to load AI model. Must be set in ENV")
    return Settings()  # type: ignore


@lru_cache
def get_settings_pretty_print() -> str:
    """Return a readable summary of key runtime settings."""
    settings = get_settings()

    lines = [
        "=== Runtime Settings ===",
        f"ENV: {settings.mode}",
        f"Base Model: {settings.model}",
        f"Prompt Source {settings.prompt_source}"
        f"Embedding Model: {settings.embedding_model}",
    ]
    return "\n".join(lines)


if __name__ == "__main__":
    pass

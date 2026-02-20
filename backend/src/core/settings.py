import os
from functools import lru_cache
from pathlib import Path
from typing import Literal, Optional, Sequence, Union

from pydantic import AnyHttpUrl, field_validator
from pydantic_core.core_schema import ValidationInfo
from pydantic_settings import BaseSettings, SettingsConfigDict
from dotenv import load_dotenv

load_dotenv()

# Points to the root directory adjust as needed
ROOT_PATH = Path(__file__).parents[2]


class AppSettings(BaseSettings):
    PROJECT_NAME: str
    MODE: Literal["testing", "dev", "production"] = "dev"
    STORAGE_SERVICE: Literal["local", "cloud"] = "local"

    BACKEND_CORS_ORIGINS: Sequence[AnyHttpUrl | str] = ()

    DATABASE_URI: str | None = None
    POSTGRES_URL: str | None = None
    SQLITE_DB_PATH: str | None = None
    PROJECT_ROOT: Path | str

    FIREBASE_CRED: str | None = None
    FIREBASE_AUTH_EMULATOR_HOST: str | None = None
    FIREBASE_STORAGE_EMULATOR_HOST: str|None = None
    STORAGE_BUCKET: str | None = None

    @field_validator("BACKEND_CORS_ORIGINS", mode="before")
    @classmethod
    def assemble_cors_origins(cls, v: str | list[str]):
        if isinstance(v, str):
            return [i.strip() for i in v.split(",")]
        return v

    @field_validator("SQLITE_DB_PATH", mode="before")
    @classmethod
    def assemble_db_connection(cls, v: str | None):
        return v or ":memory:"

    model_config = SettingsConfigDict(
        env_file=ROOT_PATH / ".env",
        env_nested_delimiter="__",
        extra="ignore",
    )


@lru_cache
def get_settings() -> AppSettings:
    valid_modes = ("testing", "dev", "production")
    env_mode = os.getenv("MODE", "dev")
    auth_emulator = os.getenv("FIREBASE_AUTH_EMULATOR_HOST", None)
    if env_mode not in valid_modes:
        raise ValueError(f"Invalid MODE: {env_mode}. Must be one of {valid_modes}")
    allowed_origins = os.getenv("ALLOWED_ORIGINS","")
    if allowed_origins:
        allowed_origins = allowed_origins.split(",")
    else:
        allowed_origins = ["http://localhost:5174"]

    if env_mode and not auth_emulator:

        raise ValueError("FIREBASE_AUTH_EMULATOR_HOST must be provided during dev env")

    app_settings = AppSettings(
        PROJECT_NAME="GestaltQuestions",
        BACKEND_CORS_ORIGINS=[] + allowed_origins,
        FIREBASE_CRED=os.getenv("FIREBASE_CRED", "default_firebase_cred"),
        STORAGE_BUCKET=os.getenv("STORAGE_BUCKET"),
        SQLITE_DB_PATH=(ROOT_PATH / Path(os.getenv("SQLITE_DB_PATH", ":memory:")))
        .resolve()
        .as_posix(),
        POSTGRES_URL=os.getenv("POSTGRES_URL"),
        PROJECT_ROOT=ROOT_PATH,
    )
    return app_settings


if __name__ == "__main__":
    print(get_settings())

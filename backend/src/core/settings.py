import os
from functools import lru_cache
from pathlib import Path
from typing import Literal

from dotenv import load_dotenv
from pydantic import field_validator, model_validator
from pydantic_settings import BaseSettings, SettingsConfigDict

load_dotenv()

# Points to the root directory adjust as needed
ROOT_PATH = Path(__file__).parents[2]


class AppSettings(BaseSettings):
    PROJECT_NAME: str
    mode: Literal["testing", "dev", "production"] = "dev"
    STORAGE_SERVICE: Literal["local", "cloud"] = "local"

    BACKEND_CORS_ORIGINS: list[str] | str = []

    DATABASE_URI: str | None = None
    POSTGRES_URL: str | None = None
    SQLITE_DB_PATH: str | None = None
    PROJECT_ROOT: Path | str

    FIREBASE_CRED: str | None = None
    FIREBASE_AUTH_EMULATOR_HOST: str | None = None
    STORAGE_EMULATOR_HOST: str | None = None
    STORAGE_BUCKET: str | None = None

    @field_validator("BACKEND_CORS_ORIGINS", mode="before")
    @classmethod
    def assemble_cors_origins(cls, v):
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

    @model_validator(mode="after")
    def validate_required_runtime_fields(self):
        required_fields = [
            "FIREBASE_CRED",
            "STORAGE_BUCKET",
        ]
        missing = []
        for field in required_fields:
            if not getattr(self, field):
                missing.append(field)
        if missing:
            raise RuntimeError(f"Missing required settings: {', '.join(missing)}")
        return self

    @model_validator(mode="after")
    def validate_emulator(self):
        firebase_emulators = ["STORAGE_EMULATOR_HOST", "FIREBASE_AUTH_EMULATOR_HOST"]
        try:
            for v in firebase_emulators:
                if self.mode == "dev":
                    if not getattr(self, v):
                        raise RuntimeError(f"{v} must be set in Dev")
                elif self.mode == "production":
                    if getattr(self, v):
                        setattr(self, v, None)
                        os.environ.pop(v, None)
                else:
                    raise ValueError(f"Cannot determine mode {self.mode}")

            return self
        except Exception:
            raise


@lru_cache
def get_settings() -> AppSettings:
    valid_modes = ("testing", "dev", "production")
    env_mode = os.getenv("MODE", "dev")
    auth_emulator = os.getenv("FIREBASE_AUTH_EMULATOR_HOST", None)
    if env_mode not in valid_modes:
        raise ValueError(f"Invalid MODE: {env_mode}. Must be one of {valid_modes}")

    allowed_origins_env = os.getenv("ALLOWED_ORIGINS", "")

    def normalize_origin(origin: str, scheme: str) -> str:
        origin = origin.strip()

        # remove scheme if already present
        if origin.startswith("http://"):
            origin = origin[len("http://") :]
        elif origin.startswith("https://"):
            origin = origin[len("https://") :]

        return f"{scheme}://{origin}"

    if allowed_origins_env:
        scheme = "https" if env_mode == "production" else "http"

        allowed_origins = [
            normalize_origin(o, scheme)
            for o in allowed_origins_env.split(",")
            if o.strip()
        ]
    else:
        allowed_origins = ["http://localhost:5174"]
    if env_mode == "dev" and not auth_emulator:
        raise ValueError("FIREBASE_AUTH_EMULATOR_HOST must be provided during dev env")

    return AppSettings(
        PROJECT_NAME="GestaltQuestions",
        BACKEND_CORS_ORIGINS=[*allowed_origins],
        SQLITE_DB_PATH=(ROOT_PATH / Path(os.getenv("SQLITE_DB_PATH", ":memory:")))
        .resolve()
        .as_posix(),
        PROJECT_ROOT=ROOT_PATH,
    )


if __name__ == "__main__":
    print(get_settings())

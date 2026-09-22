from collections.abc import Generator
from typing import Annotated

from fastapi import Depends
from sqlmodel import Session, create_engine
from functools import lru_cache
from backend.core.logger import logger
from backend.core.settings import get_settings


from .exceptions import DatabaseConfigError, DatabaseInitializationError

app_settings = get_settings()


def initialize_database_engine():
    DATABASE_URL = None
    if app_settings.ENV == "testing":
        DATABASE_URL = "sqlite:///:memory:"
    elif app_settings.ENV == "production" or app_settings.ENV == "dev":
        DATABASE_URL = app_settings.DATABASE_URL
    if not DATABASE_URL:
        raise DatabaseConfigError("Failed to initialize database. URL is not set")
    logger.info(f"[DATABASE Intialization] Success")

    try:
        connect_args = {}
        engine = create_engine(
            url=DATABASE_URL,
            echo=True,
            connect_args=connect_args,  # always a dict, never None
        )
        return engine
    except Exception as e:
        raise DatabaseInitializationError(
            f"Error initializing database engine {e}"
        ) from e

@lru_cache
def session_cache():
    return initialize_database_engine()

def get_session() -> Generator[Session, None, None]:
    engine = initialize_database_engine()
    """Yield a SQLModel session per request."""
    with Session(engine, expire_on_commit=False) as session:
        yield session


SessionDep = Annotated[Session, Depends(get_session)]


if __name__ == "__main__":
    from sqlalchemy import text

    engine = initialize_database_engine()

    try:
        with engine.connect() as conn:
            result = conn.execute(text("SELECT 1"))
            print("Database connection successful")
            print(result.scalar())

    except Exception as e:
        print("Database connection failed")
        print(e)

from collections.abc import Generator
from typing import Annotated

from fastapi import Depends
from sqlmodel import Session, SQLModel, create_engine

from src.core.logger import logger
from src.core.settings import get_settings

from .exceptions import DatabaseConfigError

app_settings = get_settings()


# Define choosing the settings
try:
    if app_settings.ENV == "testing":
        DATABASE_URL = "sqlite:///:memory:"
    else:
        DATABASE_URL = app_settings.DATABASE_URL

    if not DATABASE_URL:
        raise DatabaseConfigError("Database url is not set")
except Exception as e:
    raise DatabaseConfigError(
        f"Failed to initialized database with env set to: {app_settings.ENV}, {e}"
    ) from e
logger.info(f"[DATABASE Intialization]: Database path set to {DATABASE_URL}")

try:
    connect_args = {}
    engine = create_engine(
        url=DATABASE_URL,
        echo=True,
        connect_args=connect_args,  # always a dict, never None
    )
    Base = SQLModel
except Exception as e:
    raise RuntimeError(f"Error initializing database engine {e}")


def create_db_and_tables(engine=engine):
    Base.metadata.create_all(engine)
    return engine


def get_session() -> Generator[Session, None, None]:
    """Yield a SQLModel session per request."""
    with Session(engine, expire_on_commit=False) as session:
        yield session


SessionDep = Annotated[Session, Depends(get_session)]


if __name__ == "__main__":
    create_db_and_tables()

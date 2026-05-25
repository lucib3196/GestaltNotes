from collections.abc import Generator
from typing import Annotated

from fastapi import Depends
from sqlmodel import Session, SQLModel, create_engine

from src.core.logger import logger
from src.core.settings import get_settings

from .exceptions import DatabaseConfigError

app_settings = get_settings()


# Define choosing the settings
if app_settings.ENV == "testing":
    DATABASE_URL = "sqlite:///:memory:"
elif app_settings.ENV == "production":
    DATABASE_URL = app_settings.DATABASE_URL
elif app_settings.ENV == "dev":
    DATABASE_URL = f"sqlite:///{app_settings.DATABASE_URL}"
else:
    raise ValueError(f"Unknown environment: {app_settings.ENV}")
logger.debug(f"[DATABASE Intialization]: Database path set to {DATABASE_URL}")

try:
    if not DATABASE_URL:
        raise DatabaseConfigError("Database url is not set")
    connect_args = {}
    if app_settings.ENV == "dev" and DATABASE_URL.startswith("sqlite"):
        connect_args = {"check_same_thread": False}
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

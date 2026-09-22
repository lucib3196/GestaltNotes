import pytest
from sqlmodel import Session, SQLModel, create_engine

from backend.core.firebase import initialize_firebase_app
from backend.core.logger import logger

initialize_firebase_app()


@pytest.fixture(scope="function")
def test_engine():
    """Provide a temporary SQLite engine for testing."""
    url = "sqlite:///:memory:"
    engine = create_engine(
        url,
        echo=False,
        connect_args={"check_same_thread": False},
    )
    SQLModel.metadata.create_all(engine)
    yield engine
    engine.dispose()


@pytest.fixture(scope="function")
def db_session(test_engine):
    """Provide a new SQLModel session for each test with isolation."""
    with Session(test_engine, expire_on_commit=False) as session:
        yield session
        session.rollback()


@pytest.fixture(autouse=True)
def _clean_db(db_session, test_engine) -> None:
    """Automatically reset database tables between tests."""
    logger.debug("Cleaning Database")
    SQLModel.metadata.drop_all(test_engine)
    SQLModel.metadata.create_all(test_engine)


pytest_plugins = ["tests.support.firebase"]

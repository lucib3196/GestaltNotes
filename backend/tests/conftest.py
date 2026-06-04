import os

import pytest
import requests
from sqlmodel import Session, SQLModel, create_engine

from src.core.firebase import initialize_firebase_app
from src.core.logger import logger

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


@pytest.fixture(scope="session", autouse=True)
def verify_firebase_emulator():
    host = os.getenv("FIREBASE_AUTH_EMULATOR_HOST")

    if not host:
        pytest.fail(
            "FIREBASE_AUTH_EMULATOR_HOST is not set. "
            "Refusing to run tests against production Firebase."
        )
    assert "localhost" in host or "127.0.0.1" in host
    try:
        response = requests.get(
            f"http://{host}/",
            timeout=2,
        )
        assert response.status_code == 200
    except Exception as exc:
        pytest.fail(f"Firebase Auth Emulator is not reachable at {host}: {exc}")

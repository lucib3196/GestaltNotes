import contextlib
import os
from collections.abc import Generator
from typing import Any

import firebase_admin
import pytest

from backend.core.firebase import initialize_firebase_app

ALLOWED_EMULATOR_HOST_PREFIXES = (
    "localhost:",
    "127.0.0.1:",
    "0.0.0.0:",
    "host.docker.internal:",
    "http://localhost:",
    "http://127.0.0.1:",
    "http://0.0.0.0:",
    "http://host.docker.internal:",
)


def is_local_emulator_host(value: str | None) -> bool:
    if not value:
        return False

    return value.startswith(ALLOWED_EMULATOR_HOST_PREFIXES)


def normalize_storage_emulator_host() -> bool:
    host = os.environ.get("STORAGE_EMULATOR_HOST")
    if not host or host == "...":
        return False

    if not host.startswith(("http://", "https://")):
        os.environ["STORAGE_EMULATOR_HOST"] = f"http://{host}"

    return True


def is_safe_firebase_project() -> bool:
    project_id = os.environ.get("FIREBASE_PROJECT_ID", "")
    return project_id in {"demo-test", "gestalt-test", "firebase-emulator-test"}


def is_firebase_enabled() -> bool:
    storage_tests_enabled = os.environ.get("RUN_FIREBASE_STORAGE_TESTS") == "1"
    test_environment = os.environ.get("APP_ENV") == "test"

    auth_emulator_host = os.environ.get("FIREBASE_AUTH_EMULATOR_HOST")
    storage_emulator_host = os.environ.get("STORAGE_EMULATOR_HOST")

    auth_emulator_configured = is_local_emulator_host(auth_emulator_host)
    storage_emulator_configured = (
        is_local_emulator_host(storage_emulator_host)
        and normalize_storage_emulator_host()
    )

    return (
        test_environment
        and storage_tests_enabled
        and auth_emulator_configured
        and storage_emulator_configured
        and is_safe_firebase_project()
    )




@pytest.fixture(scope="session")
def firebase_app_for_tests() -> Generator[Any]:
    if not is_firebase_enabled():
        pytest.skip("Firebase auth emulator is not configured.")

    app = initialize_firebase_app()
    yield app

    with contextlib.suppress(Exception):
        firebase_admin.delete_app(app)

    initialize_firebase_app.cache_clear()

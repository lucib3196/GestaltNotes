import os
from collections.abc import Iterator
from urllib.parse import urlparse

import firebase_admin
import pytest
from google.auth.credentials import AnonymousCredentials

from object_store.firebase import FirebaseBlobStorage


@pytest.fixture(scope="session")
def firebase_app_for_tests() -> Iterator[firebase_admin.App]:
    if os.environ.get("RUN_FIREBASE_STORAGE_TESTS") != "1":
        pytest.skip("Set RUN_FIREBASE_STORAGE_TESTS=1 to run emulator tests.")

    host = os.environ.get("STORAGE_EMULATOR_HOST")
    if not host:
        pytest.fail("STORAGE_EMULATOR_HOST must point to the Storage emulator.")

    normalized_host = (
        host if host.startswith(("http://", "https://")) else f"http://{host}"
    )
    parsed = urlparse(normalized_host)
    if parsed.hostname not in {
        "localhost",
        "127.0.0.1",
        "firebase_emulator",
        "host.docker.internal",
    }:
        pytest.fail("Storage tests require a local emulator.")

    project_id = "demo-object-store"
    bucket = f"{project_id}.appspot.com"

    previous_host = host
    os.environ["STORAGE_EMULATOR_HOST"] = normalized_host
    try:
        app = firebase_admin.initialize_app(
            AnonymousCredentials(),
            options={
                "projectId": project_id,
                "storageBucket": bucket,
            },
        )
        try:
            yield app
        finally:
            firebase_admin.delete_app(app)
    finally:
        os.environ["STORAGE_EMULATOR_HOST"] = previous_host


@pytest.fixture
def storage(firebase_app_for_tests: firebase_admin.App) -> FirebaseBlobStorage:
    return FirebaseBlobStorage(
        bucket=firebase_app_for_tests.options["storageBucket"] # type: ignore
    )

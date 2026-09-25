from pytest import fixture

from backend.core.settings import get_settings
from backend.storage.blob.firebase import FirebaseBlobStorage


@fixture
def storage(firebase_app_for_tests):
    settings = get_settings()
    assert settings.STORAGE_BUCKET
    return FirebaseBlobStorage(bucket=settings.STORAGE_BUCKET)

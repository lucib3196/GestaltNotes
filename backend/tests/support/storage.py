from object_store import FirebaseBlobStorage
from pytest import fixture

from backend.core.settings import get_settings


@fixture
def storage(firebase_app_for_tests):
    settings = get_settings()
    assert settings.STORAGE_BUCKET
    return FirebaseBlobStorage(bucket=settings.STORAGE_BUCKET)

from pytest import fixture
from backend.storage.services.firebase_blob import FirebaseBlobStorage
from backend.core.settings import get_settings


@fixture
def storage(firebase_app_for_tests):
    settings = get_settings()
    assert settings.STORAGE_BUCKET
    return FirebaseBlobStorage(bucket=settings.STORAGE_BUCKET)

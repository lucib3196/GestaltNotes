from pathlib import Path
import json
from firebase_admin import credentials
import firebase_admin
from functools import lru_cache
from .settings import get_settings

app_settings = get_settings()


@lru_cache
def initialize_firebase_app():
    if not app_settings.FIREBASE_CRED:
        raise ValueError("Firebase Credentials Not Found")
    try:
        if app_settings.MODE == "production":
            cred = json.loads(app_settings.FIREBASE_CRED)
        else:
            cred = (
                Path(app_settings.PROJECT_ROOT) / app_settings.FIREBASE_CRED
            ).resolve()
    except Exception as e:
        raise ValueError(f"There was an error loading credentials {str(e)}")

    try:
        cred = credentials.Certificate(cred)
        bucket_name = app_settings.STORAGE_BUCKET
        if not bucket_name:
            raise ValueError("No Bucket Specified must be set in Environment")
        firebase_admin.initialize_app(cred, {"storageBucket": bucket_name})
    except Exception as e:
        raise ValueError(f"Could not initialize creditionals error {str(e)}")


if __name__ == "__main__":
    fb = initialize_firebase_app()

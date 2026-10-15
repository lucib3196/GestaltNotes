import os
from functools import lru_cache
from urllib.parse import urlparse
import socket
import firebase_admin
from firebase_admin import credentials

from .settings import get_settings
from .exceptions import FirebaseInitializationError, MissingConfigError
from .logger import logger

app_settings = get_settings()


# def _normalize_STORAGE_EMULATOR_HOST(host: str) -> str:
#     if host.startswith(("http://", "https://")):
#         return host
#     return f"http://{host}"


def _log_firebase_emulator_config() -> None:
    auth_host = os.getenv("FIREBASE_AUTH_EMULATOR_HOST")
    storage_host = os.getenv("STORAGE_EMULATOR_HOST")

    logger.debug(
        "Firebase emulator env: auth=%s storage=%s",
        auth_host,
        storage_host,
    )

    if storage_host:
        parsed = urlparse(storage_host)
        hostname = parsed.hostname
        port = parsed.port

        logger.debug(
            "Firebase storage emulator parsed: scheme=%s host=%s port=%s",
            parsed.scheme,
            hostname,
            port,
        )

        if hostname and port:
            with socket.create_connection((hostname, port), timeout=2):
                logger.info("Firebase storage emulator is reachable")


@lru_cache
def initialize_firebase_app():

    try:
        if firebase_admin._apps:
            return firebase_admin.get_app()

        if not app_settings.FIREBASE_CRED:
            raise MissingConfigError(
                "FIREBASE_CRED must be configured before Firebase initialization"
            )

        # -----------------------------
        # Handle Emulator Mode
        # -----------------------------
        if app_settings.ENV == "production":
            os.environ.pop("FIREBASE_AUTH_EMULATOR_HOST", None)
            os.environ.pop("STORAGE_EMULATOR_HOST", None)

        else:
            print("Running")
            # ensure dev env vars exist
            if not app_settings.FIREBASE_AUTH_EMULATOR_HOST:
                raise FirebaseInitializationError(
                    "FIREBASE_AUTH_EMULATOR_HOST must be set in dev"
                )

            if not app_settings.STORAGE_EMULATOR_HOST:
                raise FirebaseInitializationError(
                    "STORAGE_EMULATOR_HOST must be set in dev"
                )

            os.environ["FIREBASE_AUTH_EMULATOR_HOST"] = (
                app_settings.FIREBASE_AUTH_EMULATOR_HOST
            )
            os.environ["STORAGE_EMULATOR_HOST"] = app_settings.STORAGE_EMULATOR_HOST

            
            _log_firebase_emulator_config()

        # -----------------------------
        # Load credentials
        # -----------------------------
        cred = credentials.Certificate(app_settings.FIREBASE_CRED)

        # -----------------------------
        # Initialize Firebase
        # -----------------------------
        bucket_name = app_settings.STORAGE_BUCKET

        if not bucket_name:
            raise MissingConfigError("STORAGE_BUCKET must be defined")

        firebase_admin.initialize_app(cred, {"storageBucket": bucket_name})

        return firebase_admin.get_app()
    except MissingConfigError:
        raise
    except Exception as e:
        logger.exception(
            "Firebase initialization failed. bucket=%s emulator=%s",
            app_settings.STORAGE_BUCKET,
            os.getenv("STORAGE_EMULATOR_HOST"),
        )
        raise FirebaseInitializationError(
            f"Could not initialize firebase app: {e}"
        ) from e


if __name__ == "__main__":
    fb = initialize_firebase_app()
    print(fb)

from collections.abc import Iterator
from contextlib import contextmanager

from langchain_astradb import AstraDBVectorStore
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from object_store import BlobStorage, FirebaseBlobStorage

from backend.core import get_settings
from backend.core.exceptions import MissingConfigError
from backend.core.firebase import initialize_firebase_app
from backend.database.config import open_session
from backend.storage import FileService


def create_storage() -> BlobStorage:
    """Initialize Firebase in the calling process before opening its bucket."""
    settings = get_settings()
    if not settings.STORAGE_BUCKET:
        raise MissingConfigError("STORAGE_BUCKET must be defined")
    initialize_firebase_app()
    return FirebaseBlobStorage(settings.STORAGE_BUCKET)


@contextmanager
def file_service_scope() -> Iterator[FileService]:
    """Create a service with a fresh session and close it after use."""
    storage = create_storage()
    with open_session() as session:
        yield FileService(storage=storage, session=session)


def create_vector_store(name: str) -> AstraDBVectorStore:
    """Create embedding and vector-store clients only when vectorizing."""
    settings = get_settings()
    if not settings.ASTRA_DB_API_ENDPOINT or not settings.ASTRA_DB_APPLICATION_TOKEN:
        raise MissingConfigError("Astra DB endpoint and application token must be set")
    return AstraDBVectorStore(
        collection_name=name,
        embedding=GoogleGenerativeAIEmbeddings(model="gemini-embedding-001"),
        api_endpoint=settings.ASTRA_DB_API_ENDPOINT,
        token=settings.ASTRA_DB_APPLICATION_TOKEN,
    )

from urllib.parse import urlparse
from uuid import UUID

from langchain_astradb import AstraDBVectorStore
from langchain_core.vectorstores import VectorStore
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_postgres import PGVector
from sqlalchemy.engine import make_url
from sqlalchemy.exc import ArgumentError
from sqlmodel import Session

from backend.core import get_settings
from backend.core.exceptions import InvalidConfigError, MissingConfigError
from backend.courses.exceptions import CourseNotFoundError
from backend.courses.models import Course
from backend.courses.vector_store.models import (
    CourseVectorStore,
    VectorstoreProvider,
    VectorStoreStatus,
)


class CourseVectorStoreService:
    def __init__(self, session: Session) -> None:
        self._session = session

    def is_configured(self, course_id: UUID) -> bool:
        """Check saved configuration without contacting the vector-store provider."""
        record = self._session.get(CourseVectorStore, course_id)
        return record is not None and record.status == VectorStoreStatus.READY

    def get_configuration(self, course_id: UUID) -> CourseVectorStore | None:
        return self._session.get(CourseVectorStore, course_id)

    def configure(
        self,
        course_id: UUID,
        description: str | None = None,
        *,
        collection_name: str,
        provider: VectorstoreProvider = VectorstoreProvider.POSTGRES,
        embedding_model: str = "gemini-embedding-001",
    ) -> CourseVectorStore:
        try:
            provider = VectorstoreProvider(provider)
        except ValueError as exc:
            raise ValueError(f"Unsupported vector-store provider: {provider}") from exc
        if not collection_name.strip():
            raise ValueError("Collection name must not be empty")
        if not embedding_model.strip():
            raise ValueError("Embedding model must not be empty")

        if self._session.get(Course, course_id) is None:
            raise CourseNotFoundError(str(course_id))

        record = self._session.get(CourseVectorStore, course_id)

        if record is None:
            record = CourseVectorStore(
                course_id=course_id,
                collection_name=collection_name,
                namespace_key=f"course_{course_id.hex}",
                description=description,
                embedding_model=embedding_model,
                provider=provider,
                status=VectorStoreStatus.PENDING,
            )
        else:
            requested = {
                "collection_name": collection_name,
                "provider": provider,
                "embedding_model": embedding_model,
            }
            mismatches = [
                name
                for name, value in requested.items()
                if getattr(record, name) != value
            ]
            if mismatches:
                raise ValueError(
                    "Existing vector-store configuration differs for: "
                    + ", ".join(mismatches)
                )

        if record.status == VectorStoreStatus.ARCHIVED:
            raise ValueError("Cannot configure an archived vector store")
        if record.status == VectorStoreStatus.READY:
            return record

        try:
            record.status = VectorStoreStatus.READY
            self._session.add(record)
            self._session.commit()
        except Exception:
            self._session.rollback()
            raise

        self._session.refresh(record)
        return record

    def get_vectorstore(self, course_id: UUID) -> VectorStore:
        config = self.get_configuration(course_id)
        if config is None:
            raise LookupError(
                f"Vector-store configuration not found for course '{course_id}'"
            )

        if config.status != VectorStoreStatus.READY:
            raise ValueError(f"Vector store for course '{course_id}' is not ready")

        return self._create_vector_store(config)

    def _create_vector_store(self, record: CourseVectorStore) -> VectorStore:

        settings = get_settings()
        if not settings.GOOGLE_API_KEY or not settings.GOOGLE_API_KEY.strip():
            raise MissingConfigError("GOOGLE_API_KEY must be configured")

        if record.provider == VectorstoreProvider.POSTGRES:
            if not settings.DATABASE_URL or not settings.DATABASE_URL.strip():
                raise MissingConfigError("DATABASE_URL must be configured")
            try:
                connection_url = make_url(settings.DATABASE_URL)
            except (ArgumentError, ValueError) as exc:
                raise InvalidConfigError("DATABASE_URL is malformed") from exc
            if connection_url.get_backend_name() != "postgresql":
                raise InvalidConfigError("PGVector requires a PostgreSQL database")
            connection_url = connection_url.set(drivername="postgresql+psycopg")
        elif record.provider == VectorstoreProvider.ASTRA:
            if not (
                settings.ASTRA_DB_API_ENDPOINT
                and settings.ASTRA_DB_API_ENDPOINT.strip()
            ):
                raise MissingConfigError("ASTRA_DB_API_ENDPOINT must be configured")
            if not (
                settings.ASTRA_DB_APPLICATION_TOKEN
                and settings.ASTRA_DB_APPLICATION_TOKEN.strip()
            ):
                raise MissingConfigError(
                    "ASTRA_DB_APPLICATION_TOKEN must be configured"
                )
            try:
                endpoint = urlparse(settings.ASTRA_DB_API_ENDPOINT)
                valid_endpoint = endpoint.scheme == "https" and bool(endpoint.hostname)
            except ValueError:
                valid_endpoint = False
            if not valid_endpoint:
                raise InvalidConfigError(
                    "ASTRA_DB_API_ENDPOINT must be a valid HTTPS URL"
                )
        else:
            raise ValueError(f"Unsupported vector-store provider: {record.provider}")

        embeddings = GoogleGenerativeAIEmbeddings(
            model=record.embedding_model,
            api_key=settings.GOOGLE_API_KEY,  # type: ignore
        )
        if record.provider == VectorstoreProvider.POSTGRES:
            vector_store = PGVector(
                embeddings=embeddings,
                collection_name=record.collection_name,
                connection=connection_url.render_as_string(hide_password=False),
                use_jsonb=True,
            )
        else:
            vector_store = AstraDBVectorStore(
                collection_name=record.collection_name,
                embedding=embeddings,
                api_endpoint=settings.ASTRA_DB_API_ENDPOINT,
                token=settings.ASTRA_DB_APPLICATION_TOKEN,
            )
        return vector_store

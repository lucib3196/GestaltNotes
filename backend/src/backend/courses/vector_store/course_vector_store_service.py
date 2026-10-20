from uuid import UUID

from langchain_astradb import AstraDBVectorStore
from langchain_astradb.utils.astradb import SetupMode
from langchain_core.vectorstores import VectorStore
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from sqlmodel import Session

from backend.core import get_settings
from backend.core.exceptions import MissingConfigError
from backend.courses.exceptions import CourseNotFoundError
from backend.courses.models import Course
from backend.courses.vector_store.models import CourseVectorStore, VectorStoreStatus


def create_vector_store(
    *,
    collection_name: str,
    provider: str = "astra",
    embedding_model: str = "gemini-embedding-001",
    create_collection: bool = False,
) -> VectorStore:
    """Create embedding and vector-store clients only when vectorizing."""
    if provider != "astra":
        raise ValueError(f"Unsupported vector-store provider: {provider}")

    settings = get_settings()
    if embedding_model != settings.ASTRA_DB_EMBEDDING_MODEL:
        raise ValueError(
            "Embedding model must match the shared collection configuration"
        )
    if not settings.ASTRA_DB_API_ENDPOINT or not settings.ASTRA_DB_APPLICATION_TOKEN:
        raise MissingConfigError("Astra DB endpoint and application token must be set")
    return AstraDBVectorStore(
        collection_name=collection_name,
        embedding=GoogleGenerativeAIEmbeddings(model=embedding_model),
        api_endpoint=settings.ASTRA_DB_API_ENDPOINT,
        token=settings.ASTRA_DB_APPLICATION_TOKEN,
        setup_mode=SetupMode.SYNC if create_collection else SetupMode.OFF,
    )


class CourseVectorStoreService:
    def __init__(self, session: Session) -> None:
        self._session = session

    def is_configured(self, course_id: UUID) -> bool:
        """Check the saved association without making an Astra DB request."""
        record = self._session.get(CourseVectorStore, course_id)
        return record is not None and record.status == VectorStoreStatus.READY

    def get_configuration(self, course_id: UUID) -> CourseVectorStore | None:
        return self._session.get(CourseVectorStore, course_id)

    def create(
        self,
        course_id: UUID,
        description: str | None = None,
        *,
        collection_name: str,
        provider: str = "astra",
        embedding_model: str = "gemini-embedding-001",
    ) -> CourseVectorStore:
        if provider != "astra":
            raise ValueError(f"Unsupported vector-store provider: {provider}")
        if embedding_model != get_settings().ASTRA_DB_EMBEDDING_MODEL:
            raise ValueError(
                "Embedding model must match the shared collection configuration"
            )

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
        elif record.collection_name != collection_name:
            raise ValueError(
                "Course vector store already references a different collection"
            )

        if record.status == VectorStoreStatus.ARCHIVED:
            raise ValueError("Cannot configure an archived vector store")
        if record.provider != "astra":
            raise ValueError(f"Unsupported vector-store provider: {record.provider}")
        if record.embedding_model != get_settings().ASTRA_DB_EMBEDDING_MODEL:
            raise ValueError(
                "Embedding model must match the shared collection configuration"
            )
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

        return create_vector_store(
            collection_name=config.collection_name,
            provider=config.provider,
            embedding_model=config.embedding_model,
            create_collection=False,
        )

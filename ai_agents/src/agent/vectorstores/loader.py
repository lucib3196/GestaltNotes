"""Construct course vector stores from saved collection configuration."""

from dotenv import load_dotenv
from langchain_core.vectorstores import VectorStore
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_postgres import PGVector

from agent.core.setting import get_settings

load_dotenv()
settings = get_settings()


def build_course_vectorstore(
    *,
    collection_name: str,
    embedding_model: str,
) -> VectorStore:
    """Build a PGVector client for the given collection and embedding model."""
    embeddings = GoogleGenerativeAIEmbeddings(model=embedding_model)

    return PGVector(
        embeddings=embeddings,
        collection_name=collection_name,
        connection=settings.DATABASE_URL,  # postgresql+psycopg://...
        use_jsonb=True,
        create_extension=False,  # Provision pgvector through your migrations.
    )

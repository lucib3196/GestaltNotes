import dotenv
from sqlalchemy import create_engine
from pathlib import Path
from client import LangsmithClient

ENV_PATH = Path(__file__).resolve().parents[1] / ".env"


def load_db_engine():
    db_url = dotenv.get_key(ENV_PATH, "DB_URL")

    if not db_url:
        raise ValueError(f"DB_URL is not set in {ENV_PATH}")

    return create_engine(db_url)


def load_langsmith_client() -> LangsmithClient:

    api_key = dotenv.get_key(ENV_PATH, "LANGSMITH_API_KEY")

    base_url = dotenv.get_key(ENV_PATH, "LANGGRAPH_URL")
    if not api_key:
        raise ValueError("LANGSMITH_API_KEY is not set")
    if not base_url:
        raise ValueError("LANGGRAPH_URL is not set")
    return LangsmithClient(base_url, api_key=api_key)

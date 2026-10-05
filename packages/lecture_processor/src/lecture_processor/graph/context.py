from pydantic import BaseModel
from langchain_core.language_models import BaseChatModel


class ExtractionContext(BaseModel):
    model: BaseChatModel
    prompt: str

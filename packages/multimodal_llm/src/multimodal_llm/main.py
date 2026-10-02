from collections.abc import Iterable, Sequence

from langchain_core.language_models.chat_models import BaseChatModel
from pydantic import BaseModel

from .utils import prepare_image_payload


class Response(BaseModel):
    content: str


class MultiModalLLM:
    def __init__(self, model: BaseChatModel) -> None:
        self._llm = model

    def invoke(
        self,
        *,
        prompt: str,
        images: Sequence[bytes],
        mime_type: str,
        output_model: type[BaseModel] | None = Response,
    ):
        message = self.prepare_payload(prompt, images, mime_type)
        if output_model:
            chain = self._llm.with_structured_output(schema=output_model)
            return chain.invoke([message])
        return self._llm.invoke([message])

    async def ainvoke(
        self,
        *,
        prompt: str,
        images: Sequence[bytes],
        mime_type: str,
        output_model: type[BaseModel] | None = Response,
    ):
        message = self.prepare_payload(prompt, images, mime_type)
        if output_model:
            chain = self._llm.with_structured_output(schema=output_model)
            return await chain.ainvoke([message])
        return await self._llm.ainvoke([message])

    @staticmethod
    def prepare_payload(
        prompt: str,
        data: Iterable[bytes],
        mime_type: str,
    ):
        return {
            "role": "user",
            "content": [
                {"type": "text", "text": prompt},
                *prepare_image_payload(data, mime_type),
            ],
        }

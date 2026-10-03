from functools import lru_cache
from typing import Awaitable, Callable

from langchain.agents.middleware import AgentMiddleware, ModelRequest, ModelResponse
from langchain.chat_models import init_chat_model
from langchain_core.language_models.chat_models import BaseChatModel
from pydantic import BaseModel, Field, model_validator

from agent.config.models import MODELS_BY_PROVIDER, GeminiModel, ModelProvider


class ConfigSchema(BaseModel):
    """Configuration for graph-based dynamic model selection."""

    model_provider: ModelProvider = ModelProvider.GEMINI
    model: GeminiModel = Field(default=GeminiModel.GEMINI_3_5_FLASH)

    @model_validator(mode="after")
    def validate_model_matches_provider(self) -> "ConfigSchema":
        """Validate that the configured model belongs to its provider."""
        valid_models = MODELS_BY_PROVIDER[self.model_provider]

        if self.model not in valid_models:
            raise ValueError(
                f"Model {self.model!r} is not valid for provider {self.model_provider!r}"
            )

        return self


@lru_cache(maxsize=1)
def get_model_cache() -> dict[str, BaseChatModel]:
    """Return initialized chat models keyed by model name."""
    return {
        model.value: init_chat_model(
            model_provider=model_provider.value,
            model=model.value,
        )
        for model_provider, models in MODELS_BY_PROVIDER.items()
        for model in models
    }


def get_model(model_name: str) -> BaseChatModel:
    """Return a cached chat model by name."""
    try:
        return get_model_cache()[model_name]
    except KeyError as exc:
        available_models = ", ".join(sorted(get_model_cache()))
        raise ValueError(
            f"Unknown model {model_name!r}. Available models: {available_models}"
        ) from exc


class ModelRoutingMiddleware(AgentMiddleware):
    """Route model calls to the model selected in runtime context."""

    def wrap_model_call(  # type: ignore
        self,
        request: ModelRequest["ConfigSchema"],
        handler: Callable[[ModelRequest["ConfigSchema"]], ModelResponse],
    ) -> ModelResponse:
        """Route sync model calls through the cached model registry."""
        model_name = request.runtime.context.model
        return handler(request.override(model=get_model(model_name)))

    async def awrap_model_call(  # type: ignore
        self,
        request: ModelRequest["ConfigSchema"],
        handler: Callable[[ModelRequest["ConfigSchema"]], Awaitable[ModelResponse]],
    ) -> ModelResponse:
        """Route async model calls through the cached model registry."""
        model_name = request.runtime.context.model
        return await handler(request.override(model=get_model(model_name)))

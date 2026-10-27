from enum import StrEnum


class ModelProvider(StrEnum):
    """Supported model providers."""

    GEMINI = "google_genai"


class GeminiModel(StrEnum):
    """Supported Gemini model names."""

    GEMINI_3_5_FLASH = "gemini-3.5-flash"
    GEMINI_2_5_FLASH = "gemini-2.5-flash"
    GEMINI_2_5_FLASH_LITE = "gemini-2.5-flash-lite"
    GEMINI_2_5_PRO = "gemini-2.5-pro"


MODELS_BY_PROVIDER: dict[ModelProvider, tuple[StrEnum, ...]] = {
    ModelProvider.GEMINI: tuple(GeminiModel),
}

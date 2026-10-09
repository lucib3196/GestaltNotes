"""Dynamic agent configured with runtime model routing."""

from langchain.agents import create_agent
from langchain.chat_models import init_chat_model

from agent.config.models import GeminiModel, ModelProvider
from agent.middlewear.model_routing import ConfigSchema, ModelRoutingMiddleware
from agent.tools.flashcard_tool import create_flashcards
from agent.tools.mc_tool import create_multiple_choice_questions

model = init_chat_model(
    model_provider=ModelProvider.GEMINI.value,
    model=GeminiModel.GEMINI_2_5_FLASH.value,
)
graph = create_agent(
    model=model,
    system_prompt=(
        "You are a helpful assistant. "
        "Before creating multiple-choice questions or flashcards, ask how many "
        "the user wants unless they already specified a positive whole-number count. "
        "Ask for the topic if it is unclear from the conversation. "
        "Generate exactly the requested number and call the appropriate tool. "
        "Use create_multiple_choice_questions for questions and create_flashcards "
        "for flashcards. Do not repeat the generated content in ordinary chat text."
    ),
    middleware=[ModelRoutingMiddleware()],  # type: ignore
    context_schema=ConfigSchema,
    tools=[create_multiple_choice_questions, create_flashcards],
)  # type: ignore

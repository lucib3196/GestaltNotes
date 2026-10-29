"""Dynamic agent configured with runtime model routing."""

from pathlib import Path

from dotenv import load_dotenv
from langchain.agents import create_agent
from langchain.chat_models import init_chat_model

from agent.config.models import GeminiModel, ModelProvider
from agent.core.setting import get_settings
from agent.middlewear.model_routing import ConfigSchema, ModelRoutingMiddleware
from agent.middlewear.title_generator import ThreadTitleMiddleware
from agent.tools.flashcard_tool import create_flashcards
from agent.tools.lecture_retriever import (
    build_course_exploration_tool,
    build_retrieval_tool,
)
from agent.tools.mc_tool import create_multiple_choice_questions
from agent.tools.mermaid_diagrams import create_flowchart
from agent.tools.web_search import web_search

load_dotenv()
settings = get_settings()


model = init_chat_model(
    model_provider=ModelProvider.GEMINI.value,
    model=GeminiModel.GEMINI_2_5_FLASH.value,
)
graph = create_agent(
    model=model,
    system_prompt=(
        Path(__file__).resolve().parent / "prompts" / "chat_prompt.md"
    ).read_text(encoding="utf-8"),
    middleware=[
        ModelRoutingMiddleware(),
        ThreadTitleMiddleware(model=model),
    ],  # type: ignore
    context_schema=ConfigSchema,
    tools=[
        create_multiple_choice_questions,
        create_flashcards,
        build_retrieval_tool(summary_model=model),
        build_course_exploration_tool(summary_model=model),
        web_search,
        create_flowchart,
    ],
)  # type: ignore

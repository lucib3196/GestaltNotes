"""Dynamic agent configured with runtime model routing."""

from langchain.agents import create_agent
from langchain.chat_models import init_chat_model
from langchain_astradb import AstraDBVectorStore
from agent.config.models import GeminiModel, ModelProvider
from agent.middlewear.model_routing import ConfigSchema, ModelRoutingMiddleware
from agent.tools.flashcard_tool import create_flashcards
from agent.tools.mc_tool import create_multiple_choice_questions
from agent.tools.lecture_retriever import build_retrieval_tool
from dotenv import load_dotenv
from agent.vectorstores.loader import vector_store
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from agent.core.setting import get_settings
from agent.middlewear.title_generator import ThreadTitleMiddleware

load_dotenv()
settings = get_settings()

model = init_chat_model(
    model_provider=ModelProvider.GEMINI.value,
    model=GeminiModel.GEMINI_2_5_FLASH.value,
)
embeddings = GoogleGenerativeAIEmbeddings(model=settings.embedding_model)
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
        "You also have access to retrieve lecture content"
    ),
    middleware=[ModelRoutingMiddleware(), ThreadTitleMiddleware(model=model)],  # type: ignore
    context_schema=ConfigSchema,
    tools=[
        create_multiple_choice_questions,
        create_flashcards,
        build_retrieval_tool(
            AstraDBVectorStore(
                collection_name="me118_lecture_fb",
                embedding=embeddings,
                api_endpoint=settings.ASTRA_DB_API_ENDPOINT,
                token=settings.ASTRA_DB_APPLICATION_TOKEN,
            ),
            summary_model=model,
            name="retrieve_me118_notes",
            description="Use this to return documents from the course me118",
        ),
    ],
)  # type: ignore

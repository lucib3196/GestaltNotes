from typing import Any, Literal

from langchain.tools import ToolRuntime, tool
from pydantic import BaseModel, Field

from agent.middlewear.model_routing import ConfigSchema, get_model


class WebSearchCitation(BaseModel):
    url: str
    title: str | None = None
    start_index: int | None = Field(default=None, ge=0)
    end_index: int | None = Field(default=None, ge=0)


class WebSearchArtifact(BaseModel):
    kind: Literal["web_search"] = "web_search"
    data: list[WebSearchCitation] = Field(default_factory=list)


@tool(
    "search",
    return_direct=True,
    response_format="content_and_artifact",
    description=(
        "Search the web using Google Search for current information "
        "or external sources. Returns a search-grounded answer and "
        "source citations. Use a focused query describing the information "
        "needed."
    ),
)
async def web_search(
    query: str,
    runtime: ToolRuntime[ConfigSchema],
    num_sources: int = 3,
) -> tuple[str, dict[str, Any]]:
    model = get_model(runtime.context.model)
    model_with_search = model.bind_tools([{"google_search": {}}])
    result = await model_with_search.ainvoke(
        [
            (
                "system",
                "Use Google Search to research the user's query. "
                "Provide a concise answer grounded in the search results "
                "and cite the sources supporting your claims. "
                "If search results are unavailable or insufficient, say so. "
                "Do not invent sources or claim to have searched when you have not."
                f"Use a max of {num_sources}",
            ),
            ("human", query),
        ]
    )

    citations: list[WebSearchCitation] = []
    for block in result.content_blocks:
        if block.get("type") != "text":
            continue
        for annotation in block.get("annotations", []):
            if annotation.get("type") != "citation":
                continue
            parsed = WebSearchCitation.model_validate(
                {
                    "url": annotation.get("url"),
                    "title": annotation.get("title"),
                    "start_index": annotation.get("start_index"),
                    "end_index": annotation.get("end_index"),
                }
            )
            citations.append(parsed)

    artifact = WebSearchArtifact(data=citations)
    return result.text, artifact.model_dump(mode="json")

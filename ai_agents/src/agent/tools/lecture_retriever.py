from langchain_core.documents import Document
from langchain_core.tools import BaseTool, tool
from langchain_core.vectorstores import VectorStore
from pydantic import BaseModel
from typing import Literal, List


class ResourceArtifact(BaseModel):
    kind: Literal["retrieval"]
    name: str
    label: str | None = None
    data: List[Document]


def build_retrieval_tool(
    vector_store: VectorStore,
    *,
    name: str,
    description: str,
    label: str | None = None,
    k: int = 3,
) -> BaseTool:
    if k < 1:
        raise ValueError("k must be positive")

    @tool(
        name,
        return_direct=True,
        description=description,
        response_format="content_and_artifact",
    )
    def retrieve(query: str) -> tuple[str, list[Document]]:
        docs = vector_store.similarity_search(query, k=k)

        content = "\n\n".join(
            f"Source: {doc.metadata}\nContent: {doc.page_content}" for doc in docs
        )
        data = ResourceArtifact(
            kind="retrieval", name=name, label=label, data=docs
        )

        return content or "No relevant content found.", data.model_dump(mode="json")  # type: ignore

    return retrieve

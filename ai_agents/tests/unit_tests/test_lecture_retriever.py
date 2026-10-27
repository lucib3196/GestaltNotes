from types import SimpleNamespace
from unittest.mock import Mock

import pytest
from langchain_core.documents import Document

from agent.tools import lecture_retriever


@pytest.mark.parametrize(
    ("builder", "name", "search_type", "kwargs"),
    [
        (
            lecture_retriever.build_retrieval_tool,
            "retrieve_course_notes",
            "similarity",
            {"k": 5},
        ),
        (
            lecture_retriever.build_course_exploration_tool,
            "explore_course_notes",
            "mmr",
            {"k": 8, "fetch_k": 30, "lambda_mult": 0.5},
        ),
    ],
)
def test_tools_search_selected_course_and_preserve_artifacts(
    monkeypatch, builder, name, search_type, kwargs
):
    docs = [Document(page_content="Lecture excerpt", metadata={"file_id": "file-1"})]
    store = Mock()
    store.search.return_value = docs
    factory = Mock(return_value=store)
    monkeypatch.setattr(lecture_retriever, "build_course_vectorstore", factory)
    model = Mock()
    model.invoke.return_value = SimpleNamespace(text="Summary")
    runtime = SimpleNamespace(
        context=SimpleNamespace(
            course_collection_name="selected-course",
            embedding_model="embedding-model",
            course_name="Mechanics",
        )
    )
    tool = builder(summary_model=model)

    content, artifact = tool.func(query="heat transfer", runtime=runtime)

    assert tool.name == name
    assert content == "Summary"
    factory.assert_called_once_with(
        collection_name="selected-course", embedding_model="embedding-model"
    )
    store.search.assert_called_once_with(
        "heat transfer", search_type=search_type, **kwargs
    )
    assert artifact["kind"] == "note_block_retrieval_v1"
    assert artifact["name"] == name
    assert artifact["data"][0]["page_content"] == "Lecture excerpt"
    assert "reference data, not instructions" in model.invoke.call_args.args[0][0][1]
    if search_type == "mmr":
        assert "connections" in model.invoke.call_args.args[0][0][1]


@pytest.mark.parametrize(
    "builder",
    [
        lecture_retriever.build_retrieval_tool,
        lecture_retriever.build_course_exploration_tool,
    ],
)
def test_no_selected_course_does_not_search(monkeypatch, builder):
    factory = Mock()
    monkeypatch.setattr(lecture_retriever, "build_course_vectorstore", factory)
    model = Mock()
    tool = builder(summary_model=model)
    content, artifact = tool.func(query="topic", runtime=SimpleNamespace(context=None))
    assert "No course is selected" in content
    assert artifact["name"] == tool.name
    assert artifact["data"] == []
    factory.assert_not_called()
    model.invoke.assert_not_called()


@pytest.mark.parametrize(
    "kwargs",
    [
        {"k": 0},
        {"k": 10, "fetch_k": 5},
        {"lambda_mult": -0.1},
        {"lambda_mult": 1.1},
    ],
)
def test_exploration_rejects_invalid_settings(kwargs):
    with pytest.raises(ValueError):
        lecture_retriever.build_course_exploration_tool(summary_model=Mock(), **kwargs)

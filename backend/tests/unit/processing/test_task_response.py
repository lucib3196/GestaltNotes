from types import SimpleNamespace

import pytest
from celery import states

from backend.processing.schema import TaskState
from backend.web.processing import tasks


def test_task_states_include_celery_builtins():
    assert {state.value for state in TaskState} >= states.ALL_STATES


@pytest.mark.parametrize("state", list(TaskState))
def test_task_status_response(state, monkeypatch):
    task = SimpleNamespace(
        state=state.value,
        result=ValueError("Failed") if state == TaskState.FAILURE else {"saved": 2},
        info={"current": 1, "total": 2},
        successful=lambda: state == TaskState.SUCCESS,
        failed=lambda: state == TaskState.FAILURE,
    )
    monkeypatch.setattr(tasks, "AsyncResult", lambda *_args, **_kwargs: task)

    response = tasks.get_task_status("task-id")
    assert response.task_id == "task-id"
    assert response.status == state
    assert response.result == ({"saved": 2} if state == TaskState.SUCCESS else None)
    assert response.progress == (
        {"current": 1, "total": 2} if state == TaskState.PROGRESS else None
    )
    assert response.error == ("Failed" if state == TaskState.FAILURE else None)

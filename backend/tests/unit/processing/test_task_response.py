from types import SimpleNamespace

import pytest
from celery import states

from backend.processing.models import ProcessingStatus
from backend.web.processing import tasks


def test_task_states_include_celery_builtins():
    assert {state.value for state in ProcessingStatus} >= states.ALL_STATES


@pytest.mark.parametrize("state", list(ProcessingStatus))
def test_task_status_response(state, monkeypatch):
    task = SimpleNamespace(
        state=state.value,
        result=ValueError("Failed")
        if state == ProcessingStatus.FAILURE
        else {"saved": 2},
        info={"current": 1, "total": 2},
        successful=lambda: state == ProcessingStatus.SUCCESS,
        failed=lambda: state == ProcessingStatus.FAILURE,
    )
    monkeypatch.setattr(tasks, "AsyncResult", lambda *_args, **_kwargs: task)

    response = tasks.get_task_status("task-id")
    assert response.task_id == "task-id"
    assert response.status == state
    assert response.result == (
        {"saved": 2} if state == ProcessingStatus.SUCCESS else None
    )
    assert response.progress == (
        {"current": 1, "total": 2} if state == ProcessingStatus.PROGRESS else None
    )
    assert response.error == ("Failed" if state == ProcessingStatus.FAILURE else None)

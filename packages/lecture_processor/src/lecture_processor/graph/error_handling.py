from typing import Literal

from langgraph.errors import NodeError
from langgraph.runtime import Runtime
from langgraph.types import RetryPolicy
from pydantic import ValidationError

from .context import ExtractionContext
from .state import SectionTask, State, TaskFailure

retry_policy = RetryPolicy(
    max_attempts=3,
    initial_interval=1.0,
    backoff_factor=2.0,
    max_interval=10.0,
)


def make_task_failure(
    state: State | SectionTask,
    error: NodeError,
    runtime: Runtime[ExtractionContext],
) -> TaskFailure:
    exception = error.error
    kind: Literal["input", "provider", "validation", "unexpected"]

    if isinstance(exception, ValidationError):
        kind = "validation"
    elif isinstance(exception, (TimeoutError, ConnectionError)):
        kind = "provider"
    elif isinstance(exception, (ValueError, OSError)):
        kind = "input"
    else:
        kind = "unexpected"

    return TaskFailure(
        task=error.node,
        section_index=state.get("index") if isinstance(state, dict) else None,
        kind=kind,
        message=str(exception) or type(exception).__name__,
        attempts=(
            runtime.execution_info.node_attempt if runtime.execution_info else "unknown"
        ),
    )


def handle_node_error(
    state: State,
    error: NodeError,
    runtime: Runtime[ExtractionContext],
):
    if runtime.context.failure.policy == "strict":
        raise error.error
    return {"failures": [make_task_failure(state, error, runtime)]}

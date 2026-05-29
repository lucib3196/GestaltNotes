from uuid import UUID
from datetime import date, datetime, time
from pathlib import Path
from typing import Any
from uuid import UUID
from pydantic import BaseModel
from enum import Enum
ID = str | UUID


def convert_uuid(val: ID):
    if isinstance(val, str):
        return UUID(val)
    if isinstance(val, UUID):
        return val
    if val is None:
        return None
    raise TypeError(f"Value {val} is not type of str or UUID")


def to_serializable(obj: Any) -> Any:
    """Convert supported objects into JSON-serializable Python values."""
    if isinstance(obj, Enum):
        return obj.value
    if isinstance(obj, BaseModel):
        return obj.model_dump(mode="json")
    if isinstance(obj, dict):
        return {key: to_serializable(value) for key, value in obj.items()}
    if isinstance(obj, list):
        return [to_serializable(value) for value in obj]
    if isinstance(obj, (datetime, date, time)):
        return obj.isoformat()
    if isinstance(obj, UUID):
        return str(obj)
    if isinstance(obj, Path):
        return obj.as_posix()
    if isinstance(obj, (list, tuple, set)):
        return [to_serializable(value) for value in obj]
    
    return obj

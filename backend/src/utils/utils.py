from uuid import UUID
from typing import TypeAlias

ID = str | UUID


def convert_uuid(val: ID ):
    if isinstance(val, str):
        return UUID(val)
    elif isinstance(val, UUID):
        return val
    elif val is None:
        return None
    else:
        raise TypeError(f"Value {val} is not type of str or UUID")

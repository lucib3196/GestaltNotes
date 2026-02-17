from uuid import UUID


def convert_uuid(val: str | UUID):
    if isinstance(val, str):
        return UUID(val)
    elif isinstance(val, UUID):
        return val
    else:
        raise TypeError(f"Value {val} is not type of str or UUID")

from uuid import UUID

ID = str | UUID


def convert_uuid(val: ID):
    if isinstance(val, str):
        return UUID(val)
    if isinstance(val, UUID):
        return val
    if val is None:
        return None
    raise TypeError(f"Value {val} is not type of str or UUID")

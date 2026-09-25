from collections.abc import Iterable


def normalize_storage_key(*parts: str | Iterable[str]) -> str:
    """Join storage key parts into a normalized slash-delimited key."""
    segments: list[str] = []

    for part in parts:
        values = part if isinstance(part, Iterable) and not isinstance(part, str) else (part,)

        for value in values:
            segments.extend(segment for segment in value.split("/") if segment)

    return "/".join(segments)

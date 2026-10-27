from dataclasses import dataclass
from datetime import datetime


@dataclass
class BlobMetadata:
    key: str
    size: int | None
    content_type: str | None
    created_at: datetime | None = None
    updated_at: datetime | None = None
    checksum: str | None = None

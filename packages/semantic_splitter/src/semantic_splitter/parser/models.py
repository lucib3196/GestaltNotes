import base64

from document_processing.splitter import PageChunk
from pydantic import BaseModel, field_serializer


class PDFSection[TContent: BaseModel | str = str](BaseModel):
    """Section metadata and the original PDF pages it describes."""

    metadata: TContent
    document: PageChunk

    @field_serializer("document", when_used="json")
    def serialize_document(self, document: PageChunk) -> dict[str, str | int]:
        """Encode PDF bytes as base64 alongside their range and MIME type."""
        return {
            "content": base64.b64encode(document.content).decode("ascii"),
            "start": document.start,
            "end": document.end,
            "mime_type": document.mime_type,
        }

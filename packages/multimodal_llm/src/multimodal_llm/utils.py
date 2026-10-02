import base64
from collections.abc import Iterable


def prepare_image_payload(payload: Iterable[bytes], mime_type: str):
    return [
        {
            "type": "image_url",
            "image_url": {
                "url": f"data:{mime_type};base64,{base64.b64encode(p).decode('utf-8')}"
            },
        }
        for p in payload
    ]

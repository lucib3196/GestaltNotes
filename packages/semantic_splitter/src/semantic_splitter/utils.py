from io import BytesIO

from PIL import Image


def get_image_type(data: bytes) -> str:
    try:
        with Image.open(BytesIO(data)) as image:
            if not image.format:
                raise ValueError("Failed to determine image type")
            return image.format
    except Exception as e:
        raise ValueError(f"Failed to open image {e}")

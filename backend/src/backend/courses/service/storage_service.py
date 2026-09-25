from firebase_admin import storage
from google.cloud.storage.blob import Blob


class CourseStorageService:
    def __init__(self, bucket: str) -> None:
        self.bucket = storage.bucket(bucket)

    def course_prefix(self, course_id: str) -> str:
        return f"courses/{course_id}"

    def create_dir(self, target: str) -> str:
        key = self.to_blob_key(target)
        blob: Blob = self.bucket.blob(key)
        blob.upload_from_string(data="")
        return str(blob.name)

    def to_blob_key(self, value: str | Blob):
        if isinstance(value, Blob):
            if not value.name:
                raise ValueError(f"Cannot determine blob: {value}")
            key = value.name
        else:
            key = str(value)
        return key.replace("\\", "/").lstrip("/")

from pathlib import Path
from typing import Sequence
from firebase_admin import storage
import firebase_admin
from src.core.firebase import initialize_firebase_app
Target = str | Path

initialize_firebase_app()
class FirebaseStorage:
    def __init__(self, bucket: str):
        self.bucket = storage.bucket(bucket)
  

    def create_storage(self, target: str | Path) -> str:
        blob = self.bucket.blob(target)
        blob.upload_from_string("")
        return str(blob.name)

    def read_file(self, target: str | Path) -> bytes | None:
        try:
            blob = self.bucket.get_blob(target)
            if blob:
                return blob.download_as_bytes()
            
        except Exception as e:
            raise ValueError(f"Could not read contents from blob {e}")

    def list_files(self, target: str | Path, recursive: bool = False) -> Sequence[str]:
        if isinstance(target, Path):
            target = target.as_posix()
        if not target.endswith("/"):
            target = target + "/"

        blobs = list(self.bucket.list_blobs(prefix=target))
        if not recursive:
            result = []
            for blob in blobs:
                relative = blob.name[len(target) :]
                if "/" not in relative:
                    result.append(blob.name)
            return result
        return [blob.name for blob in blobs]
    
    def delete_file(self, target: str | Path) -> None:
        blob = self.bucket.blob(str(target))
        blob.delete()

    def upload_file(self, target: str | Path, data: bytes, content_type: str = "application/octet-stream") -> str:
        blob = self.bucket.blob(str(target))
        blob.upload_from_string(data, content_type=content_type)
        return blob.public_url


if __name__ == "__main__":
    import os
    
    FirebaseStorage(bucket="gestaltnotes.firebasestorage.app").create_storage("name")
from pathlib import Path
from firebase_admin import storage

Target = str | Path


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

    def list_files(self, target: str | Path, recursive: bool = False):
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

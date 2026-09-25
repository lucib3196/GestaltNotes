
from .blob_storage import BlobStorage
from .file_repository import FileRepository


class FileService:
    def __init__(self, storage:BlobStorage, repo: FileRepository ):
        self._storage = storage
        self._repo = repo
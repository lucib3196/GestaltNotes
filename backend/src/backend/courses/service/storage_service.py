from backend.storage.services.file_service import FileService


class CourseStorageService:
    def __init__(self, storage: FileService) -> None:
        self._storage = storage

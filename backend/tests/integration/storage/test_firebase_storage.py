from uuid import uuid4

import pytest

from backend.storage.exceptions import BlobDirectoryNotFoundError, BlobNotFoundError


def storage_key(name: str) -> str:
    return f"tests/storage/{uuid4().hex}/{name}"


async def cleanup_directory(storage, key: str) -> None:
    try:
        await storage.delete_directory(key)
    except BlobDirectoryNotFoundError:
        pass


@pytest.mark.asyncio
async def test_blob_core_operations(storage):
    key = storage_key("note.md")
    content = b"# Title\ncontent"
    content_type = "text/markdown"

    try:
        assert await storage.exists(key) is False

        await storage.upload(key, data=content, content_type=content_type)

        assert await storage.exists(key) is True
        assert await storage.read(key) == content
        assert await storage.download(key) == content

        metadata = await storage.get_metadata(key)
        assert metadata.key == key
        assert metadata.size == len(content)
        assert metadata.content_type == content_type

        await storage.delete(key)

        assert await storage.exists(key) is False
        with pytest.raises(BlobNotFoundError):
            await storage.read(key)
    finally:
        await storage.delete(key)


@pytest.mark.asyncio
async def test_missing_blob_metadata_raises_not_found(storage):
    key = storage_key("missing.md")

    with pytest.raises(BlobNotFoundError):
        await storage.get_metadata(key)


@pytest.mark.asyncio
async def test_directory_level_operations(storage):
    directory = storage_key("course-assets")
    directory_key = f"{directory}/"

    nested_file = f"{directory_key}lecture.md"
    deep_file = f"{directory_key}week-1/notes.md"

    try:
        assert await storage.directory_exists(directory) is False

        await storage.create_directory(directory)

        assert await storage.directory_exists(directory) is True

        await storage.upload(nested_file, data=b"lecture", content_type="text/markdown")
        await storage.upload(deep_file, data=b"notes", content_type="text/markdown")

        non_recursive_items = await storage.list_directory(directory)
        non_recursive_keys = {item.key for item in non_recursive_items}

        assert nested_file in non_recursive_keys
        assert deep_file not in non_recursive_keys
        assert directory_key not in non_recursive_keys

        recursive_items = await storage.list_directory(directory, recursive=True)
        recursive_keys = {item.key for item in recursive_items}

        assert nested_file in recursive_keys
        assert deep_file in recursive_keys
        assert directory_key not in recursive_keys

        await storage.delete_directory(directory)

        assert await storage.directory_exists(directory) is False
        assert await storage.exists(nested_file) is False
        assert await storage.exists(deep_file) is False
    finally:
        await cleanup_directory(storage, directory)


@pytest.mark.asyncio
async def test_delete_missing_directory_raises_not_found(storage):
    directory = storage_key("missing-directory")

    with pytest.raises(BlobDirectoryNotFoundError):
        await storage.delete_directory(directory)
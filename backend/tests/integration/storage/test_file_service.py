from uuid import uuid4

import pytest

from backend.accounts.models import User
from backend.storage.blob.exceptions import BlobNotFoundError
from backend.storage.repo.file_repository import FileRepository
from backend.storage.services.file_service import FileService


def storage_key(name: str) -> str:
    return f"tests/storage/file-service/{uuid4().hex}/{name}"


@pytest.fixture
def file_service(db_session, storage):
    repo = FileRepository(db_session, storage)
    return FileService(storage, repo)


@pytest.fixture
def file_owner(db_session):
    suffix = uuid4().hex
    user = User(
        email=f"file-service-owner-{suffix}@example.com",
        username=f"file-service-owner-{suffix}",
    )
    db_session.add(user)
    db_session.commit()
    db_session.refresh(user)
    return user


@pytest.mark.asyncio
async def test_file_service_creates_file_in_storage_and_database(
    file_service,
    storage,
    file_owner,
):
    key = storage_key("note.md")
    content = b"# Title\ncontent"

    try:
        file = await file_service.create_file(
            owner=file_owner,
            filename=key,
            data=content,
            content_type="text/markdown",
        )

        assert file.id is not None
        assert file.owner_id == file_owner.id
        assert file.original_name == "note.md"
        assert file.storage_key == key
        assert file.content_type == "text/markdown"
        assert file.size_bytes == len(content)

        assert await storage.read(key) == content

        found = await file_service.get_file(file.id)
        assert found.id == file.id
        assert found.storage_key == key
    finally:
        await storage.delete(key)


@pytest.mark.asyncio
async def test_file_service_replaces_file_contents_and_metadata(
    file_service,
    storage,
    file_owner,
):
    key = storage_key("replace.md")
    original = b"old content"
    replacement = b"new content is longer"

    try:
        file = await file_service.create_file(
            owner=file_owner,
            filename=key,
            data=original,
            content_type="text/markdown",
        )
        assert file.id is not None

        updated = await file_service.replace_file(
            file.id,
            data=replacement,
            content_type="text/plain",
        )

        assert updated.id == file.id
        assert updated.storage_key == key
        assert updated.content_type == "text/plain"
        assert updated.size_bytes == len(replacement)
        assert await storage.read(key) == replacement
    finally:
        await storage.delete(key)


@pytest.mark.asyncio
async def test_file_service_renames_file_in_storage_and_database(
    file_service,
    storage,
    file_owner,
):
    key = storage_key("old-name.md")
    new_name = "new-name.md"
    new_key = key.replace("old-name.md", new_name)
    content = b"rename me"

    try:
        file = await file_service.create_file(
            owner=file_owner,
            filename=key,
            data=content,
            content_type="text/markdown",
        )
        assert file.id is not None

        renamed = await file_service.rename_file(file.id, new_name)

        assert renamed.id == file.id
        assert renamed.original_name == new_name
        assert renamed.storage_key == new_key

        assert await storage.read(new_key) == content
        with pytest.raises(BlobNotFoundError):
            await storage.read(key)
    finally:
        await storage.delete(key)
        await storage.delete(new_key)


@pytest.mark.asyncio
async def test_file_service_deletes_file_from_storage_and_database(
    file_service,
    storage,
    file_owner,
):
    key = storage_key("delete.md")
    content = b"delete me"

    file = await file_service.create_file(
        owner=file_owner,
        filename=key,
        data=content,
        content_type="text/plain",
    )
    assert file.id is not None

    await file_service.delete_file(file.id)

    assert await file_service._repo.get(file.id) is None
    with pytest.raises(BlobNotFoundError):
        await storage.read(key)

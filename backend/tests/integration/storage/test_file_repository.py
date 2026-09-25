from unittest.mock import Mock
from uuid import uuid4

import pytest

from backend.accounts.models import User
from backend.storage.repo.file_repository import FileRepository
from backend.storage.repo.schema import File, FileUpdate


def storage_key(name: str) -> str:
    return f"tests/storage/{uuid4().hex}/{name}"


@pytest.fixture
def file_repository(db_session):
    return FileRepository(db_session, Mock())


@pytest.fixture
def file_owner(db_session):
    suffix = uuid4().hex
    user = User(
        email=f"storage-owner-{suffix}@example.com",
        username=f"storage-owner-{suffix}",
    )
    db_session.add(user)
    db_session.commit()
    db_session.refresh(user)
    return user


def make_file(file_owner: User) -> File:
    assert file_owner.id is not None
    return File(
        owner_id=file_owner.id,
        original_name="note.md",
        storage_key=storage_key("note.md"),
        content_type="text/markdown",
        size_bytes=12,
    )


@pytest.mark.asyncio
async def test_file_repository_creates_file(file_repository, file_owner):
    file = await file_repository.create(make_file(file_owner))

    assert file.id is not None
    assert file.owner_id == file_owner.id
    assert file.original_name == "note.md"
    assert file.content_type == "text/markdown"
    assert file.size_bytes == 12


@pytest.mark.asyncio
async def test_file_repository_gets_file(file_repository, file_owner):
    file = await file_repository.create(make_file(file_owner))
    assert file.id is not None

    found = await file_repository.get(file.id)

    assert found is not None
    assert found.id == file.id
    assert found.storage_key == file.storage_key


@pytest.mark.asyncio
async def test_file_repository_lists_files_by_owner(file_repository, file_owner):
    file = await file_repository.create(make_file(file_owner))

    files = await file_repository.list_by_owner(file_owner)

    assert [owner_file.id for owner_file in files] == [file.id]


@pytest.mark.asyncio
async def test_file_repository_updates_file(file_repository, file_owner):
    file = await file_repository.create(make_file(file_owner))
    assert file.id is not None
    original_updated_at = file.updated_at

    updated = await file_repository.update_by_id(
        file.id,
        FileUpdate(content_type="text/plain", size_bytes=42),
    )

    assert updated.content_type == "text/plain"
    assert updated.size_bytes == 42
    assert updated.updated_at >= original_updated_at


@pytest.mark.asyncio
async def test_file_repository_deletes_file(file_repository, file_owner):
    file = await file_repository.create(make_file(file_owner))
    assert file.id is not None

    await file_repository.delete(file.id)

    assert await file_repository.get(file.id) is None

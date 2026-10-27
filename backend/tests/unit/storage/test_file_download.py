import asyncio
from threading import Event
from types import SimpleNamespace
from unittest.mock import AsyncMock, Mock
from uuid import uuid4

import pytest
from object_store import FirebaseBlobStorage
from object_store.exceptions import BlobNotFoundError, BlobStorageReadError

from backend.web.storage.files import get_file


@pytest.mark.asyncio
async def test_firebase_download_does_not_block_event_loop():
    storage = FirebaseBlobStorage.__new__(FirebaseBlobStorage)
    loop = asyncio.get_running_loop()
    started = loop.create_future()
    release = Event()
    blob = Mock()

    def download(**_kwargs):
        loop.call_soon_threadsafe(started.set_result, None)
        if not release.wait(timeout=2):
            raise TimeoutError("The event loop did not release the download")
        return b"%PDF-test"

    blob.download_as_bytes.side_effect = download
    storage._bucket = Mock()
    storage._bucket.get_blob.return_value = blob
    storage._rewrite_emulator_media_link = Mock()

    task = asyncio.create_task(storage.download("lecture.pdf"))
    try:
        await asyncio.wait_for(started, timeout=3)
    finally:
        release.set()
    assert await task == b"%PDF-test"
    storage._rewrite_emulator_media_link.assert_called_once_with(blob)
    blob.download_as_bytes.assert_called_once_with(timeout=60)


@pytest.mark.asyncio
@pytest.mark.parametrize("failure", [None, RuntimeError("network unavailable")])
async def test_firebase_download_preserves_errors(failure):
    storage = FirebaseBlobStorage.__new__(FirebaseBlobStorage)
    storage._bucket = Mock()
    storage._bucket.get_blob.return_value = None
    storage._bucket.get_blob.side_effect = failure
    expected = BlobStorageReadError if failure else BlobNotFoundError
    with pytest.raises(expected):
        await storage.download("missing.pdf")


@pytest.mark.asyncio
@pytest.mark.parametrize("by_key", [True, False])
async def test_file_endpoint_returns_complete_binary_response(by_key):
    data = b"%PDF-test\n" * 100
    file = SimpleNamespace(
        original_name="Lecture 1.pdf", content_type="application/pdf"
    )
    service = SimpleNamespace(download_file=AsyncMock(return_value=(file, data)))
    file_id = None if by_key else uuid4()
    storage_key = "courses/lecture.pdf" if by_key else None

    response = await get_file(service, Mock(), file_id, storage_key)

    assert response.body == data
    assert response.headers["content-length"] == str(len(data))
    assert response.headers["content-type"] == "application/pdf"
    assert (
        response.headers["content-disposition"]
        == "inline; filename*=UTF-8''Lecture%201.pdf"
    )
    service.download_file.assert_awaited_once_with(file_id, storage_key=storage_key)

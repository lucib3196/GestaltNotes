from typing import Any
import httpx


class LangsmithClient:
    def __init__(self, base_url: str, api_key: str, timeout: float = 10):
        self._base_url = base_url.rstrip("/")
        self._timeout = timeout
        self._request_headers = {
            "X-API-Key": api_key,
            "Content-Type": "application/json",
        }

    async def get_thread(self, thread_id: str) -> dict[str, Any]:
        url = f"{self._base_url}/threads/{thread_id}"

        async with httpx.AsyncClient(
            headers=self._request_headers,
            timeout=self._timeout,
        ) as client:
            response = await client.get(url)

        response.raise_for_status()
        return response.json()




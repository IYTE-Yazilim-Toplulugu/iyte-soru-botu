import httpx
from typing import Optional, Dict, Any


class ServiceClient:
    """HTTP client for communicating with backend services."""

    def __init__(self, base_url: str, timeout: int = 30):
        self.base_url = base_url.rstrip("/")
        self.timeout = timeout

    async def get(
        self,
        path: str,
        headers: Optional[Dict[str, str]] = None,
        params: Optional[Dict[str, Any]] = None,
    ) -> httpx.Response:
        """Make GET request to service."""
        async with httpx.AsyncClient(timeout=self.timeout) as client:
            url = f"{self.base_url}{path}"
            response = await client.get(url, headers=headers, params=params)
            return response

    async def post(
        self,
        path: str,
        json_data: Optional[Dict[str, Any]] = None,
        headers: Optional[Dict[str, str]] = None,
    ) -> httpx.Response:
        """Make POST request to service."""
        async with httpx.AsyncClient(timeout=self.timeout) as client:
            url = f"{self.base_url}{path}"
            response = await client.post(url, json=json_data, headers=headers)
            return response

    async def put(
        self,
        path: str,
        json_data: Optional[Dict[str, Any]] = None,
        headers: Optional[Dict[str, str]] = None,
    ) -> httpx.Response:
        """Make PUT request to service."""
        async with httpx.AsyncClient(timeout=self.timeout) as client:
            url = f"{self.base_url}{path}"
            response = await client.put(url, json=json_data, headers=headers)
            return response

    async def delete(
        self, path: str, headers: Optional[Dict[str, str]] = None
    ) -> httpx.Response:
        """Make DELETE request to service."""
        async with httpx.AsyncClient(timeout=self.timeout) as client:
            url = f"{self.base_url}{path}"
            response = await client.delete(url, headers=headers)
            return response

    async def patch(
        self,
        path: str,
        json_data: Optional[Dict[str, Any]] = None,
        headers: Optional[Dict[str, str]] = None,
    ) -> httpx.Response:
        """Make PATCH request to service."""
        async with httpx.AsyncClient(timeout=self.timeout) as client:
            url = f"{self.base_url}{path}"
            response = await client.patch(url, json=json_data, headers=headers)
            return response

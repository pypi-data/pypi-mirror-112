"""AL-KO: Api"""
import async_timeout
import logging

from asyncio import get_event_loop
from aiohttp import ClientSession, ClientResponse
from abc import ABC, abstractmethod

from .exceptions import AlkoAuthenticationException, AlkoException


class AlkoClient(ABC):
    """Connection to AL-KO API."""

    def __init__(self, session: ClientSession) -> None:
        """Initialize the auth."""
        self._session = session

    @abstractmethod
    async def async_get_access_token(self) -> str:
        """Return a valid access token."""

    async def get(self, url: str, **kwargs) -> ClientResponse:
        """Make a GET request."""
        return await self.request("GET", url, **kwargs)

    async def patch(self, url: str, **kwargs) -> ClientResponse:
        """Make a PATCH request."""
        return await self.request("PATCH", url, **kwargs)

    async def request(self, method, url, **kwargs) -> ClientResponse:
        """Make a request."""
        headers = kwargs.get("headers")

        if headers is None:
            headers = {}
        else:
            headers = dict(headers)

        access_token = await self.async_get_access_token()

        headers["authorization"] = f"Bearer {access_token}"
        headers["Content-Type"] = "application/json"

        async with async_timeout.timeout(20, loop=get_event_loop()):
            response: ClientResponse = await self._session.request(
                method,
                url,
                headers=headers,
                **kwargs,
            )
        if response.status != 200:
            if response.status == 401:
                raise AlkoAuthenticationException(
                    {
                        "request": {
                            "method": method,
                            "url": url,
                            "headers": headers,
                            **kwargs,
                        },
                        "response": await response.json(),
                        "status": response.status,
                    }
                )
            else:
                raise AlkoException(
                    {
                        "request": {
                            "method": method,
                            "url": url,
                            "headers": headers,
                            **kwargs,
                        },
                        "response": await response.json(),
                        "status": response.status,
                    }
                )
        return response

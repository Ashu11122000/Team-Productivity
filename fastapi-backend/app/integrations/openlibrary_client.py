"""
Open Library API client.

Responsible for communicating with the external
Open Library API.

Documentation:
https://openlibrary.org/developers/api
"""

from typing import Any

import httpx

from app.core.config import settings
from app.core.logging import logger


class OpenLibraryClient:
    """Client for the Open Library REST API."""

    def __init__(self) -> None:
        self.base_url = settings.OPEN_LIBRARY_BASE_URL

    async def search_books(
        self,
        query: str,
        limit: int = 10,
    ) -> dict[str, Any]:
        """
        Search books by title, author or keyword.
        """

        endpoint = f"{self.base_url}/search.json"

        params = {
            "q": query,
            "limit": limit,
        }

        async with httpx.AsyncClient(timeout=10) as client:

            response = await client.get(
                endpoint,
                params=params,
            )

            response.raise_for_status()

            logger.info(
                "Open Library search completed.",
                query=query,
            )

            return response.json()

    async def get_book(
        self,
        work_key: str,
    ) -> dict[str, Any]:
        """
        Retrieve a book using its work key.

        Example:
        /works/OL45883W
        """

        endpoint = f"{self.base_url}{work_key}.json"

        async with httpx.AsyncClient(timeout=10) as client:

            response = await client.get(endpoint)

            response.raise_for_status()

            logger.info(
                "Book details retrieved.",
                work_key=work_key,
            )

            return response.json()

    async def get_author(
        self,
        author_key: str,
    ) -> dict[str, Any]:
        """
        Retrieve author information.

        Example:
        /authors/OL23919A
        """

        endpoint = f"{self.base_url}{author_key}.json"

        async with httpx.AsyncClient(timeout=10) as client:

            response = await client.get(endpoint)

            response.raise_for_status()

            logger.info(
                "Author details retrieved.",
                author_key=author_key,
            )

            return response.json()
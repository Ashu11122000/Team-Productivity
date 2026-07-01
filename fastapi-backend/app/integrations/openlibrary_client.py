"""
Open Library API client.

Responsible for communicating with the external
Open Library API.

Documentation:
https://openlibrary.org/developers/api
"""

from typing import Any, Final

import httpx

from app.core.config import settings
from app.core.logging import logger


class OpenLibraryClient:
    """Client for the Open Library REST API."""

    DEFAULT_TIMEOUT: Final[int] = 10
    DEFAULT_LIMIT: Final[int] = 10
    MAX_LIMIT: Final[int] = 100

    def __init__(self) -> None:
        self.base_url = settings.OPEN_LIBRARY_BASE_URL.rstrip("/")

    async def search_books(
        self,
        query: str,
        limit: int = DEFAULT_LIMIT,
    ) -> dict[str, Any]:
        """
        Search books by title, author, or keyword.
        """

        query = query.strip()
        limit = max(1, min(limit, self.MAX_LIMIT))

        if not query:
            raise ValueError("Search query cannot be empty.")

        params = {
            "q": query,
            "limit": limit,
        }

        try:
            async with httpx.AsyncClient(
                base_url=self.base_url,
                timeout=self.DEFAULT_TIMEOUT,
                follow_redirects=True,
            ) as client:

                response = await client.get(
                    "/search.json",
                    params=params,
                )

                response.raise_for_status()

                logger.info(
                    "Open Library search completed.",
                    query=query,
                    limit=limit,
                    status_code=response.status_code,
                )

                return response.json()

        except httpx.HTTPStatusError as exc:
            logger.exception(
                "Open Library returned an error.",
                query=query,
                status_code=exc.response.status_code,
            )
            raise

        except httpx.RequestError as exc:
            logger.exception(
                "Unable to connect to Open Library.",
                query=query,
                error=str(exc),
            )
            raise

    async def get_book(
        self,
        work_key: str,
    ) -> dict[str, Any]:
        """
        Retrieve a book using its work key.

        Example:
        /works/OL45883W
        """

        work_key = work_key.strip()

        if not work_key:
            raise ValueError("Work key cannot be empty.")

        try:
            async with httpx.AsyncClient(
                base_url=self.base_url,
                timeout=self.DEFAULT_TIMEOUT,
                follow_redirects=True,
            ) as client:

                response = await client.get(f"{work_key}.json")

                response.raise_for_status()

                logger.info(
                    "Book details retrieved.",
                    work_key=work_key,
                    status_code=response.status_code,
                )

                return response.json()

        except httpx.HTTPStatusError as exc:
            logger.exception(
                "Book lookup failed.",
                work_key=work_key,
                status_code=exc.response.status_code,
            )
            raise

        except httpx.RequestError as exc:
            logger.exception(
                "Failed to connect to Open Library.",
                work_key=work_key,
                error=str(exc),
            )
            raise

    async def get_author(
        self,
        author_key: str,
    ) -> dict[str, Any]:
        """
        Retrieve author information.

        Example:
        /authors/OL23919A
        """

        author_key = author_key.strip()

        if not author_key:
            raise ValueError("Author key cannot be empty.")

        try:
            async with httpx.AsyncClient(
                base_url=self.base_url,
                timeout=self.DEFAULT_TIMEOUT,
                follow_redirects=True,
            ) as client:

                response = await client.get(f"{author_key}.json")

                response.raise_for_status()

                logger.info(
                    "Author details retrieved.",
                    author_key=author_key,
                    status_code=response.status_code,
                )

                return response.json()

        except httpx.HTTPStatusError as exc:
            logger.exception(
                "Author lookup failed.",
                author_key=author_key,
                status_code=exc.response.status_code,
            )
            raise

        except httpx.RequestError as exc:
            logger.exception(
                "Failed to connect to Open Library.",
                author_key=author_key,
                error=str(exc),
            )
            raise
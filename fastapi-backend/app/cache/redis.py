"""
Redis client.

This module centralizes all Redis operations for the
Team Productivity Platform.

Current Responsibilities:
- Create Redis connection
- Health checks
- Basic cache operations

Future Responsibilities:
- JWT blacklist
- Session storage
- Rate limiting
- Distributed locks
- Celery broker
- Pub/Sub
- Cache invalidation
- Analytics caching
"""

from __future__ import annotations

from typing import Any

import redis

from app.core.config import settings
from app.core.logging import logger


class RedisClient:
    """
    Wrapper around the Redis client.

    Provides a centralized interface for cache operations.
    """

    def __init__(self) -> None:
        self._client = redis.Redis.from_url(
            settings.REDIS_URL,
            decode_responses=True,
        )

    @property
    def client(self) -> redis.Redis:
        """
        Return the underlying Redis client.
        """
        return self._client

    def ping(self) -> bool:
        """
        Verify Redis connectivity.
        """
        try:
            self._client.ping()

            logger.info(
                "Redis connection established.",
            )

            return True

        except redis.RedisError as exc:
            logger.exception(
                "Redis connection failed.",
                error=str(exc),
            )

            return False

    def get(self, key: str) -> str | None:
        """
        Retrieve a value from Redis.
        """
        return self._client.get(key)

    def set(
        self,
        key: str,
        value: Any,
        expire: int | None = None,
    ) -> bool:
        """
        Store a value in Redis.

        Args:
            key:
                Cache key.

            value:
                Value to store.

            expire:
                Expiration time in seconds.
        """
        return bool(
            self._client.set(
                name=key,
                value=value,
                ex=expire,
            )
        )

    def delete(self, key: str) -> int:
        """
        Delete a cache key.
        """
        return self._client.delete(key)

    def exists(self, key: str) -> bool:
        """
        Check whether a cache key exists.
        """
        return bool(self._client.exists(key))

    def expire(
        self,
        key: str,
        seconds: int,
    ) -> bool:
        """
        Set a key expiration time.
        """
        return bool(
            self._client.expire(
                key,
                seconds,
            )
        )

    def flush(self) -> None:
        """
        Remove all cache entries.

        Intended for development and testing only.
        """
        self._client.flushdb()

        logger.warning(
            "Redis cache flushed.",
        )

    def close(self) -> None:
        """
        Close the Redis connection.
        """
        try:
            self._client.close()

            logger.info(
                "Redis connection closed.",
            )

        except redis.RedisError as exc:
            logger.exception(
                "Failed to close Redis connection.",
                error=str(exc),
            )


redis_client = RedisClient()
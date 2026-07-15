"""In-memory rate limiter for API endpoints.

Purpose:
    Prevents abuse by limiting requests per IP within a time window.
    Uses a sliding window algorithm with automatic cleanup.

Does NOT do:
    - Persist rate limit state (resets on server restart)
    - Work across multiple instances (in-memory only)

Who depends on this:
    Rate-limited endpoints use rate_limiter_dependency as a FastAPI dependency.
"""

from __future__ import annotations

import time
from collections.abc import Callable
from typing import Any

from fastapi import HTTPException, Request, status


class InMemoryRateLimiter:
    def __init__(self, requests: int = 10, window_seconds: int = 60) -> None:
        self._requests = requests
        self._window = window_seconds
        self._buckets: dict[str, list[float]] = {}

    def _cleanup(self, key: str) -> None:
        now = time.monotonic()
        timestamps = self._buckets.get(key, [])
        cutoff = now - self._window
        self._buckets[key] = [t for t in timestamps if t > cutoff]

    def check(self, key: str) -> bool:
        self._cleanup(key)
        return len(self._buckets.get(key, [])) < self._requests

    def increment(self, key: str) -> None:
        self._cleanup(key)
        if key not in self._buckets:
            self._buckets[key] = []
        self._buckets[key].append(time.monotonic())

    def remaining(self, key: str) -> int:
        self._cleanup(key)
        return max(0, self._requests - len(self._buckets.get(key, [])))

    def reset_in(self, key: str) -> int:
        timestamps = self._buckets.get(key, [])
        if not timestamps:
            return 0
        elapsed = time.monotonic() - min(timestamps)
        return max(0, int(self._window - elapsed))


def rate_limiter_dependency(requests: int = 10, window: int = 60) -> Callable[[Request], Any]:
    limiter = InMemoryRateLimiter(requests=requests, window_seconds=window)

    async def _rate_limit(request: Request) -> None:
        key = f"{request.url.path}:{request.client.host if request.client else 'unknown'}"
        if not limiter.check(key):
            raise HTTPException(
                status_code=status.HTTP_429_TOO_MANY_REQUESTS,
                detail="Too many requests. Please try again later.",
                headers={
                    "Retry-After": str(limiter.reset_in(key)),
                    "X-RateLimit-Remaining": str(limiter.remaining(key)),
                },
            )
        limiter.increment(key)

    return _rate_limit

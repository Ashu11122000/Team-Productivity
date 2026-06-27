import time

from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request


class ResponseTimeMiddleware(BaseHTTPMiddleware):
    """
    Adds request processing time to every response.
    """

    async def dispatch(self, request: Request, call_next):
        start_time = time.perf_counter()

        response = await call_next(request)

        process_time = time.perf_counter() - start_time

        response.headers["X-Process-Time"] = f"{process_time:.6f}"

        return response
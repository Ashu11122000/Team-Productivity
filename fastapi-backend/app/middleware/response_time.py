from time import perf_counter

from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from starlette.responses import Response

from app.core.logging import logger


class ResponseTimeMiddleware(BaseHTTPMiddleware):
    """
    Adds request processing time to every response.
    """

    async def dispatch(self, request: Request, call_next) -> Response:
        start_time = perf_counter()

        try:
            response = await call_next(request)
        except Exception:
            logger.exception(
                "Failed while processing request.",
                method=request.method,
                path=request.url.path,
            )
            raise

        process_time = perf_counter() - start_time

        response.headers["X-Process-Time"] = f"{process_time:.6f}"
        response.headers["X-Process-Time-MS"] = f"{process_time * 1000: .2f}"
 
        logger.debug(
            "Request processing time recorded.",
            method=request.method,
            path=request.url.path,
            duration_ms=round(process_time * 1000, 2),
        )

        return response
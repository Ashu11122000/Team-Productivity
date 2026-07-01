from starlette.middleware.base import BaseHTTPMiddleware
from time import perf_counter

from starlette.requests import Request
from starlette.responses import Response

from app.core.logging import logger


class RequestLoggingMiddleware(BaseHTTPMiddleware):
    """
    Logs every incoming HTTP request and outgoing response.
    """

    async def dispatch(self, request: Request, call_next) -> Response:
        start_time = perf_counter()
        
        logger.info(
            "Incoming request",
            method=request.method,
            path=request.url.path,
            query=str(request.url.query),
            client=request.client.host if request.client else None,
        )
        
        try:
            response = await call_next(request)
        except Exception:
            logger.exception(
                "Unhandled exception during request processing.",
                method=request.method,
                path=request.url.path,
            )
            raise
        
        
        duration_ms = round((perf_counter() - start_time) * 1000, 2)
        logger.info(
            "Request completed",
            method=request.method,
            path=request.url.path,
            status_code=response.status_code,
            duration_ms=duration_ms,
        )

        return response
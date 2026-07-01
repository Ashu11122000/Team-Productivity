"""
Rate Limiting configuration for Team Productivity Platform.

Features:
- Global rate limiting using SlowAPI
- Client IP-based limiting 
- Standardized error response
- Easy integration with FastAPI
"""

from fastapi import FastAPI, Request, status
from fastapi.responses import JSONResponse
from slowapi import Limiter
from slowapi.errors import RateLimitExceeded
from slowapi.middleware import SlowAPIMiddleware
from slowapi.util import get_remote_address
from app.core.config import settings

# Rate Limiter
limiter = Limiter(key_func = get_remote_address, default_limits = [settings.RATE_LIMIT_DEFAULT])

# Exception Handler
def rate_limit_exceeded_handler(request: Request, exc: RateLimitExceeded) -> JSONResponse:
    """
    Handles rate limit exceeded exceptions and returns a standardized response.
    """
    
    return JSONResponse(
        status_code = status.HTTP_429_TOO_MANY_REQUESTS,
        headers = {
            "Retry-After": "60"
        },
        content = {
            "success": False,
            "message": "Rate limit exceeded. Please Try again later.",
            "error": {
                "type": "RATE_LIMIT_EXCEEDED",
                "detail": str(exc),
            },
            "path": request.url.path,
        },
    )
    
# Configuration
def configure_rate_limiter(app: FastAPI) -> None:
    """
    Configure SlowAPI middleware and exception handlers.
    """
    
    app.state.limiter = limiter
    
    app.add_exception_handler(RateLimitExceeded, rate_limit_exceeded_handler)
    
    app.add_middleware(SlowAPIMiddleware)
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from starlette.responses import Response
from app.core.config import logger

class SecurityHeadersMiddleware(BaseHTTPMiddleware):
    """
    Adds common HTTP security headers.
    """

    async def dispatch(self, request: Request, call_next) -> Response:
        try:
            response = await call_next(request)
        except Exception:
            logger.exception("Failed while applying security headers.",
            method=request.method,
            path=request.url.path,    
            )
            raise 
        
        response.headers["X-Content-Type-Options"] = "nosniff"
        response.headers["X-Frame-Options"] = "DENY"
        response.headers["Strict-Transport-Security"] = ("max-age=31536000; includeSubDomains")
        response.headers["X-XSS-Protection"] = "1; mode=block"
        response.headers["Referrer-Policy"] = "strict-origin-when-cross-origin"
        response.headers["Permissions-Policy"] = (
            "camera=(), microphone=(), geolocation=()"
        )
        response.headers["Cross-Origin-Opener-Policy"] = "same-origin"
        response.headers["Cross-Origin-Resource-Policy"] = "same-origin"
        response.headers["Content-Security-Policy"] = (
            "default-src 'self'; "
            "img-src 'self' data: https:; "
            "style-src 'self' 'unsafe-inline'; "
            "script-src 'self'; "
            "font-src 'self' https:;"
        )
        response.headers["Origin-Agent-Cluster"] = "?1"
        
        logger.debug(
            "Security headers applied.",
            path=request.url.path,
        )
        
        return response
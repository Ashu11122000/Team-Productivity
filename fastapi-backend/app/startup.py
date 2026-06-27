from app.core.logging import logger


async def startup() -> None:
    """
    Application startup tasks.

    Future:
    - Redis
    - Sentry
    - Background Scheduler
    - WebSocket Manager
    - Cache Warm-up
    """

    logger.info("Starting Team Productivity Platform FastAPI Service")


async def shutdown() -> None:
    """
    Application shutdown tasks.

    Future:
    - Close Redis
    - Close HTTP Clients
    - Flush Logs
    - Stop Background Workers
    """

    logger.info("Shutting down Team Productivity Platform FastAPI Service")
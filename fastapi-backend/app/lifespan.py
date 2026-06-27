from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.startup import shutdown, startup


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    FastAPI application lifespan.

    Responsible for:
    - Startup initialization
    - Graceful shutdown
    """

    await startup()

    yield

    await shutdown()
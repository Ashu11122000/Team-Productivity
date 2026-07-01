"""
Logging configuration for Team Productivity Platform.

Features
--------
- Structured logging using structlog
- JSON logs in production
- Console logs in development
- UTC timestamps
- Module-aware loggers
- Compatible with FastAPI, Uvicorn and SQLAlchemy
"""

from __future__ import annotations

import logging
import logging.config
import sys

import structlog

from app.core.config import settings


LOG_LEVEL = getattr(logging, settings.LOG_LEVEL.upper(), logging.INFO)

LOGGING_CONFIG: dict = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "default": {
            "()": structlog.stdlib.ProcessorFormatter,
            "processor": (
                structlog.processors.JSONRenderer()
                if settings.LOG_JSON
                else structlog.dev.ConsoleRenderer(colors=True)
            ),
        },
    },
    "handlers": {
        "default": {
            "class": "logging.StreamHandler",
            "formatter": "default",
            "stream": sys.stdout,
        },
    },
    "root": {
        "handlers": ["default"],
        "level": LOG_LEVEL,
    },
}


logging.config.dictConfig(LOGGING_CONFIG)

shared_processors = [
    structlog.contextvars.merge_contextvars,
    structlog.stdlib.add_logger_name,
    structlog.stdlib.add_log_level,
    structlog.processors.TimeStamper(fmt="iso", utc=True),
    structlog.processors.StackInfoRenderer(),
    structlog.processors.format_exc_info,
    structlog.processors.CallsiteParameterAdder(
        {
            structlog.processors.CallsiteParameter.FILENAME,
            structlog.processors.CallsiteParameter.FUNC_NAME,
            structlog.processors.CallsiteParameter.LINENO,
        }
    ),
]


structlog.configure(
    processors=[
        *shared_processors,
        structlog.stdlib.ProcessorFormatter.wrap_for_formatter,
    ],
    wrapper_class=structlog.make_filtering_bound_logger(LOG_LEVEL),
    logger_factory=structlog.stdlib.LoggerFactory(),
    cache_logger_on_first_use=True,
)

def get_logger(name: str | None = None) -> structlog.stdlib.BoundLogger:
    """
    Return a structured logger.

    Example:
        logger = get_logger(__name__)
        logger.info("User created", user_id=user.id)
    """
    return structlog.get_logger(name)


# Default application logger
logger = get_logger("app")
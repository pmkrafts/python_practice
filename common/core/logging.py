"""Structured logging configuration using loguru."""

import sys

from loguru import logger


def configure_logging(json_format: bool = False, level: str = "INFO") -> None:
    """Configure global loguru logger.

    Args:
        json_format: If True, emit logs as JSON.
        level: Minimum log level to capture.
    """
    logger.remove()

    if json_format:
        logger.add(
            sys.stdout,
            level=level,
            serialize=True,
            format="{message}",
        )
    else:
        logger.add(
            sys.stdout,
            level=level,
            format="<green>{time:YYYY-MM-DD HH:mm:ss}</green> | "
            "<level>{level:<8}</level> | "
            "<cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> - "
            "<level>{message}</level>",
        )


def get_logger(name: str | None = None):
    """Return a loguru logger bound with an optional name."""
    if name:
        return logger.bind(name=name)
    return logger

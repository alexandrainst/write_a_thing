"""Utility functions for the project."""

import logging
from functools import cache

logger = logging.getLogger("write_a_thing")


@cache
def log_once(message: str, level: int = logging.INFO) -> None:
    """Log a message.

    Args:
        message:
            The message to log.
        level:
            The logging level to use. Defaults to logging.INFO.

    Raises:
        ValueError:
            If the provided logging level is invalid.
    """
    match level:
        case logging.DEBUG:
            logger.debug(message)
        case logging.INFO:
            logger.info(message)
        case logging.WARNING:
            logger.warning(message)
        case logging.ERROR:
            logger.error(message)
        case logging.CRITICAL:
            logger.critical(message)
        case _:
            raise ValueError(f"Invalid log level: {level}")

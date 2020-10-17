"""These are just some utilities used by the single server."""
from single import _enums as enums
from loguru import logger
import sys


def set_logging_level(logging_level: enums.LoggingLevel) -> None:
    """This sets the logging level without the use of an environment variable.

    Args:
        logging_level: The logging level.

    Returns:
        Nothing.
    """
    logger.remove()
    logger.add(sys.stderr, level=logging_level.value)


def ml_error(*message: str) -> None:
    """This prints out a multi line error message.

    Args:
        *message: The message.

    Returns:
        Nothing.
    """
    combined_msg = " ".join(message)

    for line in combined_msg.splitlines():
        logger.error(line)

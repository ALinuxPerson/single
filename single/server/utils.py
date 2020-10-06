from single.server import enums
from single.core import ProviderMetadata
from single.constants import PROVIDERS_DIRS
from single import utils
from pathlib import Path
import loguru as log
import typing as t
import sys

# noinspection PyTypeChecker
logger: "log.Logger" = None  # type: ignore  # will be initialized later


def initialize_logger(logger_: "log.Logger") -> None:
    global logger

    logger = logger_


def set_logging_level(logging_level: enums.LoggingLevel) -> None:
    logger.remove()
    logger.add(sys.stderr, level=logging_level.value)


def load_providers(provider_list: t.List[ProviderMetadata]) -> None:
    logger.debug("Loading the providers....")


def ml_error(*message: str) -> None:
    combined_msg = " ".join(message)

    for line in combined_msg:
        logger.error(line)


def find_providers(dirs: t.List[Path] = None) -> t.List[Path]:
    """This finds providers from directories.

    Args:
        dirs: The directories.

    Returns:
        A list of paths which could be providers.
    """
    logger.debug("Finding providers...")
    dirs = dirs or PROVIDERS_DIRS
    logger.debug(f"Directories chosen: {utils.prettify_list(dirs)}")
    for dir_ in dirs:
        if not dir_.exists():
            logger.debug(f"Directory {dir_} doesn't exist, continuing.")
            dirs.remove(dir_)
    dirs_iterdir = [dir_.iterdir() for dir_ in dirs]
    all_paths = utils.flatten_list(dirs_iterdir)
    return [path for path in all_paths if path.is_dir()]

import errno
import sys
from loguru import logger
import os
import rpyc as rpc  # type: ignore
from rpyc.utils.server import ThreadedServer  # type: ignore
from single.constants import POSSIBLE_LOGGING_LEVELS, SOURCES_DIRS
from single import core as sc
from single import UnsupportedSystemError
import typing as t
from pathlib import Path
from single import utils as u
from toml.decoder import TomlDecodeError  # type: ignore
from single._models import ServerState

PORT = 0
loaded_sources: t.List[sc.SourceMetadata] = []
errors: t.List[Exception] = []


def find_sources(dirs: t.List[Path] = None) -> t.List[Path]:
    """This finds sources from directories.

    Args:
        dirs: The directories.

    Returns:
        A list of paths which could be sources.
    """
    logger.debug("Finding sources...")
    dirs = dirs or SOURCES_DIRS
    logger.debug(f"Directories chosen: {u.prettify_list(dirs)}")
    for dir_ in dirs:
        if not dir_.exists():
            logger.debug(f"Directory {dir_} doesn't exist, continuing.")
            dirs.remove(dir_)
    dirs_iterdir = [dir_.iterdir() for dir_ in dirs]
    all_paths = u.flatten_list(dirs_iterdir)
    return [path for path in all_paths if path.is_dir()]


def get_sources(dirs: t.List[Path] = None) -> t.List[sc.SourceMetadata]:
    """This gets sources from multiple directories.

    Args:
        dirs: The directories to get sources from.

    Returns:
        A list of Source Metadata.
    """
    dirs = dirs or SOURCES_DIRS
    sources_found = find_sources(dirs)
    source_metadata_found: t.List[sc.SourceMetadata] = []

    for source in sources_found:
        try:
            source_metadata = sc.SourceMetadata.from_source(source)
        except FileNotFoundError as error:
            ml_error(
                f"Source is not loaded (path is '{source}')\n"
                f"One or more files are missing: {error}"
            )
            errors.append(error)
            continue
        except AttributeError as error:
            ml_error(
                f"Source is not loaded (path is '{source}')\n"
                f"A package or a source reference is missing: {error}"
            )
            errors.append(error)
            continue
        except TomlDecodeError as error:
            ml_error(
                f"Source is not loaded (path is '{source}')\n"
                f"The TOML configuration couldn't be read properly: {error}"
            )
            errors.append(error)
            continue

        try:
            source_metadata.source_reference().supported()
        except UnsupportedSystemError as error:
            ml_error(
                f"Source '{source_metadata.name}' is not loaded\n"
                f"Your system is unsupported:\n"
                f"{error.message}\n"
                f"Action needed:\n"
                f"{error.action_needed}"
            )
            errors.append(error)
            continue

        logger.info(f"Loaded source '{source_metadata.name}'")
        source_metadata_found.append(source_metadata)

    logger.info(f"{len(source_metadata_found)}/{len(sources_found)} sources loaded")
    return source_metadata_found


def ml_error(message: str) -> None:
    for line in message.splitlines():
        logger.error(line)


def verify_logging_level(level: str) -> bool:
    if level not in POSSIBLE_LOGGING_LEVELS:
        logger.warning(
            f"Level '{level}' is not a valid logging level, falling back to INFO"
        )
        return False
    return True


def set_logging_level(level: str) -> None:
    if not verify_logging_level(level):
        level = "INFO"
    logger.remove()
    logger.add(sys.stderr, level=level)


def load_sources() -> None:
    global loaded_sources

    logger.info("Loading sources...")
    loaded_sources = get_sources()


def set_ports() -> None:
    global PORT

    env_port = os.getenv("SINGLES_PORT", "25000")
    logger.debug("Checking ports...")
    try:
        PORT = int(env_port)
        logger.debug(f"Setting ports to {PORT}")
    except ValueError:
        logger.error(f"Port '{env_port}' is invalid!")
        sys.exit(1)


def init() -> None:
    set_logging_level(os.getenv("SINGLES_LOGGING_LEVEL", "INFO"))
    logger.debug("Initializing server...")
    set_ports()
    load_sources()


def start() -> None:
    init()
    logger.info(f"Starting server and listening in port {PORT}...")
    try:
        server = ThreadedServer(SinglePackageManagerService, port=PORT)
        server.start()
    except OSError as error:
        if error.errno == errno.EADDRINUSE:
            logger.critical(f"Port {PORT} is already in use")
        else:
            raise


class SinglePackageManagerService(rpc.Service):
    @staticmethod
    def exposed_reload_sources() -> None:
        logger.info("Reloading sources...")
        load_sources()

    @staticmethod
    def exposed_status() -> ServerState:
        return ServerState(len(errors) == 0, errors)


if __name__ == "__main__":
    start()

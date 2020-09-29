import errno
import sys
from loguru import logger
import os
import rpyc as rpc  # type: ignore
from rpyc.utils.server import ThreadedServer  # type: ignore
from single.constants import POSSIBLE_LOGGING_LEVELS
from single import core as sc
from single import UnsupportedSystemError
import typing as t

PORT = 0
loaded_sources: t.List[sc.SourceMetadata] = []
errors: t.List[Exception] = []


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

    try:
        loaded_sources = sc.get_sources()
    except UnsupportedSystemError as error:
        ml_error(
            f"Couldn't load all sources: from source '{error.source_origin}'\n"
            f"Message:\n"
            f"{error.message}\n"
            f"Action Needed:\n"
            f"{error.action_needed}\n"
            f"Regular functionality may be hindered."
        )
        errors.append(error)


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


if __name__ == "__main__":
    start()

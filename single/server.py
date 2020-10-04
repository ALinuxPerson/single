import errno
import sys
from loguru import logger
import os
import rpyc as rpc  # type: ignore
from rpyc.utils.server import ThreadedServer  # type: ignore
from single.constants import POSSIBLE_LOGGING_LEVELS, PROVIDERS_DIRS
from single import core as sc
from single import UnsupportedSystemError
import typing as t
from pathlib import Path
from single import utils as u
from toml.decoder import TomlDecodeError  # type: ignore
from single._models import ServerState

PORT = 0
loaded_providers: t.List[sc.ProviderMetadata] = []
errors: t.List[Exception] = []


def find_providers(dirs: t.List[Path] = None) -> t.List[Path]:
    """This finds providers from directories.

    Args:
        dirs: The directories.

    Returns:
        A list of paths which could be providers.
    """
    logger.debug("Finding providers...")
    dirs = dirs or PROVIDERS_DIRS
    logger.debug(f"Directories chosen: {u.prettify_list(dirs)}")
    for dir_ in dirs:
        if not dir_.exists():
            logger.debug(f"Directory {dir_} doesn't exist, continuing.")
            dirs.remove(dir_)
    dirs_iterdir = [dir_.iterdir() for dir_ in dirs]
    all_paths = u.flatten_list(dirs_iterdir)
    return [path for path in all_paths if path.is_dir()]


def get_providers(dirs: t.List[Path] = None) -> t.List[sc.ProviderMetadata]:
    """This gets providers from multiple directories.

    Args:
        dirs: The directories to get providers from.

    Returns:
        A list of Provider Metadata.
    """
    dirs = dirs or PROVIDERS_DIRS
    providers_found = find_providers(dirs)
    provider_metadata_found: t.List[sc.ProviderMetadata] = []

    for provider in providers_found:
        try:
            provider_metadata = sc.ProviderMetadata.from_provider(provider)
        except FileNotFoundError as error:
            ml_error(
                f"Provider is not loaded (path is '{provider}')\n"
                f"One or more files are missing: {error}"
            )
            errors.append(error)
            continue
        except AttributeError as error:
            ml_error(
                f"Provider is not loaded (path is '{provider}')\n"
                f"A package or a source reference is missing: {error}"
            )
            errors.append(error)
            continue
        except TomlDecodeError as error:
            ml_error(
                f"Provider is not loaded (path is '{provider}')\n"
                f"The TOML configuration couldn't be read properly: {error}"
            )
            errors.append(error)
            continue

        try:
            provider_metadata.source_reference().supported()
        except UnsupportedSystemError as error:
            ml_error(
                f"Provider '{provider_metadata.name}' is not loaded\n"
                f"Your system is unsupported:\n"
                f"{error.message.capitalize()}\n"
                f"Action needed:\n"
                f"{error.action_needed.capitalize()}"
            )
            errors.append(error)
            continue

        logger.info(f"Loaded provider '{provider_metadata.name}'")
        provider_metadata_found.append(provider_metadata)

    logger.info(
        f"{len(provider_metadata_found)}/{len(providers_found)} providers loaded"
    )
    return provider_metadata_found


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


def load_providers() -> None:
    global loaded_providers

    logger.info("Loading providers...")
    loaded_providers = get_providers()


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
    load_providers()


def start() -> None:
    init()
    logger.info(f"Starting server and listening in port {PORT}...")
    try:
        server = ThreadedServer(SinglePackageManagerService, port=PORT)
        server.start()
    except OSError as error:
        if error.errno == errno.EADDRINUSE:
            logger.critical(f"Port {PORT} is already in use")
            sys.exit(1)
        else:
            raise
    except OverflowError:
        logger.critical(f"Port {PORT} is not within 0-65535.")
        sys.exit(1)


class SinglePackageManagerService(rpc.Service):
    @staticmethod
    def exposed_reload_providers() -> None:
        logger.info("Reloading providers...")
        load_providers()

    @staticmethod
    def exposed_status() -> ServerState:
        logger.info(f"Being asked to check the status of the server")
        return ServerState(len(errors) == 0, errors)

    def on_connect(self, conn):
        logger.info(f"A client has been connected to the server")

    def on_disconnect(self, conn):
        logger.info(f"A client has disconnected from the server")


if __name__ == "__main__":
    start()

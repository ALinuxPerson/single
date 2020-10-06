from single.server import enums
from single.server import utils
from single.core import ProviderMetadata
from loguru import logger
import typing as t

providers: t.List[ProviderMetadata] = []


def prepare_server(logging_level: enums.LoggingLevel) -> None:
    utils.initialize_logger(logger)
    utils.set_logging_level(logging_level)
    logger.debug("Preparing to start the server...")


def start(port: int, logging_level: enums.LoggingLevel) -> None:
    pass

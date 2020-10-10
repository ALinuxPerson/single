from single import enums
from single.server import utils
from single.core import ProviderMetadata
from loguru import logger
from rpyc.utils.server import ThreadedServer
from rpyc import Service
import typing as t
import errno
import sys

providers: t.List[ProviderMetadata] = []
errors: t.List[Exception] = []


def prepare_server(logging_level: enums.LoggingLevel) -> None:
    utils.initialize_logger(logger)
    utils.set_logging_level(logging_level)
    logger.debug("Preparing to start the server...")
    utils.load_providers(providers, errors)


def start(port: int, logging_level: enums.LoggingLevel) -> None:
    prepare_server(logging_level)
    try:
        server = SingleThreadedServer(SinglePackageManagerService, port=port)
        server.start()
    except OverflowError:
        logger.critical(f"The port {port} is not within 0-65535.")
        sys.exit(1)
    except PermissionError:
        logger.critical(f"The server is not allowed to use the port {port}.")
        sys.exit(1)
    except OSError as error:
        if error.errno == errno.EADDRINUSE:
            logger.critical(f"The port {port} is already in use.")
            sys.exit(1)
        else:
            raise


class SingleThreadedServer(ThreadedServer):
    def _serve_client(self, sock, credentials):
        client_host, client_port = sock.getpeername()
        if credentials:
            logger.info(
                f"A client ({client_host}) has connected to the server using the port {client_port} "
                f"(creds is {credentials})"
            )
        else:
            logger.info(
                f"A client ({client_host}) has connected to the server using the port {client_port}"
            )
        super()._serve_client(sock, credentials)

    def start(self):
        logger.debug("Listening...")
        self._listen()
        logger.debug("Registering...")
        self._register()
        logger.info(f"Server is now active and is listening on port {self.port}")
        try:
            while self.active:
                self.accept()
        except EOFError:
            logger.info("Server closed by another thread")
        except KeyboardInterrupt:
            logger.info("A keyboard interrupt has been received, stopping server")
        finally:
            logger.info("The server has been terminated")
            self.close()


class SinglePackageManagerService(Service):
    def exposed_status(self) -> None:
        pass

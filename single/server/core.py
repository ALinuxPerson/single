"""These are some critical functions and classes for core single server functionality."""
from single import _enums as enums, Package
from single.server import utils
from single.core import ProviderMetadata
from single.utils import ServerState
from loguru import logger
from rpyc.utils.server import ThreadedServer
from rpyc import Service
import typing as t
import errno
import sys

providers: t.List[ProviderMetadata] = []
errors: t.List[Exception] = []


def prepare_server(logging_level: enums.LoggingLevel) -> None:
    """This prepares the server for starting.

    Args:
        logging_level: The logging level.

    Returns:
        Nothing.
    """
    utils.initialize_logger(logger)
    utils.set_logging_level(logging_level)
    logger.debug("Preparing to start the server...")
    utils.load_providers(providers, errors)


def start(port: int, logging_level: enums.LoggingLevel) -> None:
    """This starts the server.

    Args:
        port: The port to broadcast the server on.
        logging_level: The logging level.

    Returns:
        Nothing.
    """
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
    @staticmethod
    def exposed_reload_providers() -> None:
        """This reloads providers.

        Returns:
            Nothing.
        """
        logger.info("Being asked to reload the providers")
        utils.load_providers(providers, errors)

    @property
    def exposed_status(self) -> ServerState:
        """This gets the current status of the server, including all recoverable errors found.

        Returns:
            The status of the server.
        """
        logger.info("Being asked to get the status of the server")
        return ServerState.from_errors(errors)

    @staticmethod
    def exposed_search(
        packages: t.List[str], providers_: t.List[ProviderMetadata]
    ) -> t.List[Package]:
        """This searches for packages in all providers (or some).

        Args:
            packages: The packages to search for.
            providers_: The providers to search packages from.

        Returns:
            A list of packages found.
        """
        raise NotImplementedError

    @staticmethod
    def exposed_install(
        packages: t.List[str], providers_: t.List[ProviderMetadata]
    ) -> None:
        """This installs packages by finding and installing them from different providers.

        Args:
            packages: The packages to install.
            providers_: The providers to search and install packages from.

        Returns:
            Nothing.
        """
        raise NotImplementedError

    @staticmethod
    def exposed_remove(
        packages: t.List[str], providers_: t.List[ProviderMetadata]
    ) -> None:
        """This removes packages from different providers if they are from a register.

        Args:
            packages: The packages to remove.
            providers_: The provider to remove packages from.

        Returns:
            Nothing.
        """
        raise NotImplementedError

    @staticmethod
    def exposed_update(
        packages: t.List[str], providers_: t.List[ProviderMetadata]
    ) -> None:
        """This updates packages from different providers. If the package list is empty then it will try to update
        all packages.

        Warnings:
            This function may raise an exception if the packages aren't empty and there is a provider which doesn't
            support partial upgrades.

        Args:
            packages: The packages to update.
            providers_: The providers to find updates from.

        Returns:
            Nothing.
        """
        raise NotImplementedError

    def on_disconnect(self, conn) -> None:
        logger.info("A client has disconnected from the server")

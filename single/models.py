"""These are the common core models to inherit from when creating a provider."""
import attr
from single.enums import Flags
import typing as t


@attr.s(auto_attribs=True, frozen=True)
class Package:
    """This class only provides metadata for a package.

    This class only provides metadata for a package. In order to install this, you must install it through
    its respective method in its source, usually install_package.

    Attributes:
        name: The name of the package.
        version: The version of the package.
        install_size: The install size of the package.
        download_size: The download size of the package.
    """

    name: str
    version: str
    description: str
    install_size: float
    download_size: float


@attr.s(auto_attribs=True)
class Source:
    context: "Context"

    @property
    def FLAGS(self) -> t.List[Flags]:
        """This returns the number of flags that this source uses.

        Returns:
            The flags.
        """
        raise NotImplementedError

    @property
    def backend_version(self) -> str:
        """This returns the backend version of the source.

        Returns:
            The backend version.
        """
        raise NotImplementedError

    def supported(self) -> None:
        """This goes through a number of checks to see if the source supports a system.

        Returns:
            Nothing, or raise an UnsupportedSystemError.
        """
        raise NotImplementedError

    def package(self, name: str) -> t.List[Package]:
        """This searches for packages.

        Args:
            name: The name of the package.

        Returns:
            A list of packages found.
        """
        raise NotImplementedError

    def install_package(self, *packages: Package) -> None:
        """This installs a package.

        Args:
            *packages: The packages to install.

        Returns:
            Nothing, or raise an exception.
        """
        raise NotImplementedError

    def remove_package(self, *packages: Package) -> None:
        """This removes a package.

        Args:
            *packages: The packages to remove.

        Returns:
            Nothing, or raise an exception.
        """
        raise NotImplementedError

    def update_package(self, *packages: Package) -> None:
        """This updates a package.

        This updates a package. Please not that if the PARTIAL_UPGRADES_SUPPORTED flag is not present, inputting
        anything to *packages will fail.

        Args:
            *packages: The packages to update.

        Returns:

        """
        raise NotImplementedError


@attr.s(auto_attribs=True)
class Context:
    """This is the context system.

    The context system is a way for sources, servers and clients to "speak" with each other.
    This is also an argument for sources now.
    This is the theoretical path ways for speaking:
    Source -> Server -> Client
    Source -> Client
    Source -> Server
    There is only one way communication as of now.

    There are 3 planned contexts:

    VoidContext:
        This is just a placeholder context that doesn't output a message. This is useful if you only want to
        interact with the sources directly without any daemon or client interference.

    ServerContext:
        This is a way for the sources to directly log a message to the server. This can be used as a "welcome"
        when a source is loaded, for example.

    ClientContext:
        This is a way for the sources to directly log a message to the server. Of course, the server still
        needs to intercept the logging messages for this to work, maybe put an 'context' argument to
        {install,remove,update}_packages, maybe?
    """

    def debug(self, *message: str) -> None:
        """Print a debug message.

        Args:
            *message: The message.

        Returns:
            Nothing.
        """
        raise NotImplementedError

    def info(self, *message: str) -> None:
        """Print an info message.

        Args:
            *message: The message.

        Returns:
            Nothing.
        """
        raise NotImplementedError

    def warn(self, *message: str) -> None:
        """Print a warning message.

        Args:
            *message: The message.

        Returns:
            Nothing.
        """
        raise NotImplementedError

    def error(self, *message: str) -> None:
        """Print an error message.

        Args:
            *message: The message.

        Returns:
            Nothing.
        """
        raise NotImplementedError

    def critical(self, *message: str) -> None:
        """Print a critical message.

        Args:
            *message: The message.

        Returns:
            Nothing.
        """
        raise NotImplementedError

"""These are the common core models to inherit from when creating a provider."""
import attr
from single.context import VoidContext, Context
from single.enums import System
from single import utils
from single.exceptions import UnsupportedSystemError
import typing as t
import abc


@attr.s(auto_attribs=True, frozen=True)
class Package(abc.ABC):
    """This class only provides metadata for a package.

    This class only provides metadata for a package. In order to install this, you must install it through
    its respective method in its source, usually install_package.

    Attributes:
        name: The name of the package.
        version: The version of the package.
        install_size: The install size of the package.
        download_size: The download size of the package.
        original_source: The original source of the package.
    """

    name: str
    version: str
    description: str
    install_size: float
    download_size: float
    original_source: "Source"


@attr.s(auto_attribs=True)
class Source(abc.ABC):
    context: Context = VoidContext()

    @property
    @abc.abstractmethod
    def os_supported(self) -> t.List[System]:
        """This returns the operating systems supported by this source.

        Returns:
            The operating systems supported.
        """

    @property
    @abc.abstractmethod
    def backend_version(self) -> str:
        """This returns the backend version of the source.

        Returns:
            The backend version.
        """

    @abc.abstractmethod
    def supported(self) -> None:
        """This goes through a number of checks to see if the source supports a system.

        Notes:
            It is highly recommended that you put a `super().supported()` line on your source here.

        Returns:
            Nothing, or raise an UnsupportedSystemError.
        """
        system = utils.system()
        os_supported_values = [os.value for os in self.os_supported]
        if system not in self.os_supported:
            raise UnsupportedSystemError(
                f"your system, {system.value}, is not compatible with this source.",
                f"switch to the operating systems {utils.prettify_list(os_supported_values)} or contact the developers "
                f"of this provider to make compatibility with your operating system.",
            )

    @abc.abstractmethod
    def package(self, *names: str) -> t.List[Package]:
        """This searches for packages.

        Args:
            *names: The name of the packages.

        Returns:
            A list of packages found.
        """

    @abc.abstractmethod
    def install_package(self, *packages: Package) -> None:
        """This installs a package.

        Args:
            *packages: The packages to install.

        Returns:
            Nothing, or raise an exception.
        """

    @abc.abstractmethod
    def remove_package(self, *packages: Package) -> None:
        """This removes a package.

        Args:
            *packages: The packages to remove.

        Returns:
            Nothing, or raise an exception.
        """

    @abc.abstractmethod
    def update_package(self, *packages: Package) -> None:
        """This updates a package.

        This updates a package. Please not that if the PARTIAL_UPGRADES_SUPPORTED flag is not present, inputting
        anything to *packages will fail.

        Args:
            *packages: The packages to update.

        Returns:

        """

    @abc.abstractmethod
    def greet(self) -> None:
        """This is a simple greeting once a source is initialized.

        Usually a source is initialized on post processing.
        Of course, if you don't want a greeting you can just add `pass` instead.

        Returns:
            Nothing.
        """

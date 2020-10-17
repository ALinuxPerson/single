"""These are the common core models to inherit from when creating a provider."""
import attr
from single.context import VoidContext, Context
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
    """

    name: str
    version: str
    description: str
    install_size: float
    download_size: float


@attr.s(auto_attribs=True)
class Source(abc.ABC):
    context: Context = VoidContext()

    @property
    @abc.abstractmethod
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

    def greet(self) -> None:
        """This is a simple greeting once a source is initialized.

        Usually a source is initialized on post processing.
        Of course, if you don't want a greeting you can just add `pass` instead.

        Returns:
            Nothing.
        """
        raise NotImplementedError

"""These are the common core models to inherit from when creating a source."""
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
    install_size: float
    download_size: float


class Source:
    @property
    def FLAGS(self) -> t.List[Flags]:
        raise NotImplementedError

    @property
    def version(self) -> str:
        raise NotImplementedError

    def supported(self) -> bool:
        raise NotImplementedError

    def package(self, name: str) -> t.List[Package]:
        raise NotImplementedError

    def install_package(self, package: Package) -> None:
        raise NotImplementedError

    def remove_package(self, package: Package) -> None:
        raise NotImplementedError

    def update_package(self, package: Package) -> None:
        raise NotImplementedError

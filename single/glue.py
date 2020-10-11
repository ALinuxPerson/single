"""These are the "glue" or the objects holding the server and ide together in order to have some fancy ide features."""
import attr
from single._models import Glue, ServerState
from single.core import ProviderMetadata
from single import Package
import typing as t


@attr.s(auto_attribs=True)
class SinglePackageManager(Glue):
    @property
    def status(self) -> ServerState:
        """This gets the current status of the server, including all recoverable errors found.

        Returns:
            The status of the server.
        """
        return self._conn.root.status

    def reload_providers(self) -> None:
        """This reloads providers.

        Returns:
            Nothing.
        """
        return self._conn.root.reload_providers()

    def search(
        self, packages: t.List[str], providers_: t.List[ProviderMetadata]
    ) -> t.List[Package]:
        """This searches for packages in all providers (or some).

        Args:
            packages: The packages to search for.
            providers_: The providers to search packages from.

        Returns:
            A list of packages found.
        """
        return self._conn.root.search(packages, providers_)

    def install(
        self, packages: t.List[str], providers_: t.List[ProviderMetadata]
    ) -> None:
        """This installs packages by finding and installing them from different providers.

        Args:
            packages: The packages to install.
            providers_: The providers to search and install packages from.

        Returns:
            Nothing.
        """
        return self._conn.root.install(packages, providers_)

    def remove(
        self, packages: t.List[str], providers_: t.List[ProviderMetadata]
    ) -> None:
        """This removes packages from different providers if they are from a register.

        Args:
            packages: The packages to remove.
            providers_: The provider to remove packages from.

        Returns:
            Nothing.
        """
        return self._conn.root.remove(packages, providers_)

    def update(
        self, packages: t.List[str], providers_: t.List[ProviderMetadata]
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
        return self._conn.root.update(packages, providers_)

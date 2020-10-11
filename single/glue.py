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
        return self._conn.root.status

    def reload_providers(self) -> None:
        return self._conn.root.reload_providers()

    def search(
        self, packages: t.List[str], providers_: t.List[ProviderMetadata]
    ) -> t.List[Package]:
        return self._conn.root.search(packages, providers_)

    def install(
        self, packages: t.List[str], providers_: t.List[ProviderMetadata]
    ) -> None:
        return self._conn.root.install(packages, providers_)

    def remove(
        self, packages: t.List[str], providers_: t.List[ProviderMetadata]
    ) -> None:
        return self._conn.root.remove(packages, providers_)

    def update(
        self, packages: t.List[str], providers_: t.List[ProviderMetadata]
    ) -> None:
        return self._conn.root.update(packages, providers_)

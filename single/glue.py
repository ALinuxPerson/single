import attr
from single._models import Glue, ServerState


@attr.s(auto_attribs=True)
class SinglePackageManager(Glue):
    @property
    def status(self) -> ServerState:
        return self._conn.root.status

    def reload_providers(self) -> None:
        return self._conn.root.reload_providers()

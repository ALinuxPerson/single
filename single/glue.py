import rpyc  # type: ignore
import attr


@attr.s(auto_attribs=True)
class SinglePackageManager:
    host: str
    port: int
    _conn: rpyc.Connection = attr.ib(init=False, repr=False)

    def connect(self) -> None:
        self._conn = rpyc.connect(self.host, self.port)

    def reload_providers(self) -> None:
        return self._conn.root.reload_providers()

    def status(self) -> None:
        return self._conn.root.status()

    def __attrs_post_init__(self) -> None:
        self.connect()

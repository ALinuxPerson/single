import rpyc
import attr


@attr.s(auto_attribs=True)
class SinglePackageManager:
    host: str
    port: int
    _conn: rpyc.Connection = attr.ib(init=False, repr=False)

    def connect(self) -> None:
        self._conn = rpyc.connect(self.host, self.port)

    def reload_sources(self) -> None:
        return self._conn.root.reload_sources()

    def __attrs_post_init__(self) -> None:
        self.connect()

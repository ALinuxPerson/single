import attr
import typing as t
from pathlib import Path
import rpyc
from rpyc.utils.factory import unix_connect


@attr.s(auto_attribs=True, frozen=True)
class ServerState:
    ok: bool
    errors: t.List[Exception]


@attr.s(auto_attribs=True)
class Glue:
    _conn: rpyc.Connection

    @classmethod
    def from_host(cls, host: str, port: int) -> "Glue":
        conn = rpyc.connect(host, port)

        return cls(conn)

    @classmethod
    def from_unix_socket(cls, path: Path) -> "Glue":
        conn = unix_connect(str(path))

        return cls(conn)

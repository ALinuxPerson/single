import attr
import typing as t


@attr.s(auto_attribs=True, frozen=True)
class ServerState:
    ok: bool
    errors: t.List[Exception]

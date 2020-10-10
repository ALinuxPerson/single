"""These are some models that can only be overridden within the `single` package."""
import attr
import typing as t
from pathlib import Path
import rpyc  # type: ignore
from rpyc.utils.factory import unix_connect  # type: ignore


@attr.s(auto_attribs=True, frozen=True)
# TODO: Move this class to a better file; models is supposed to be only for classes that need to be overridden.
class ServerState:
    """This is the server state.

    Args:
        ok: Whether or not the server is in an okay state or not.
        errors: The recoverable errors found.
    """

    ok: bool
    errors: t.List[Exception]

    @classmethod
    def from_errors(cls, errors: t.List[Exception]) -> "ServerState":
        """This constructs a server state object from an error list, presumably from a server.

        Args:
            errors: The list of errors.

        Returns:
            The server state.
        """
        return cls(len(errors) == 0, errors)


@attr.s(auto_attribs=True)
class Glue:
    """This is a "glue".

    This is a "glue"; meaning a way to connect the server and the ide so that auto completion and syntax highlighting
    can be present.

    This is also merely just helper methods that other classes should override just to make things a little easier.

    Args:
        _conn: The connection to the server. You shouldn't use this; you should instead use the helper class methods
               like from_host and from_unix_socket.
    """

    _conn: rpyc.Connection

    @classmethod
    def from_host(cls, host: str, port: int) -> "Glue":
        """This establishes a connection to a server using a hostname and a port (ip addresses are also accepted).

        Args:
            host: The host (or ip address).
            port: The port.

        Returns:
            A "glue" object with a connection established from a hostname and a port.
        """
        conn = rpyc.connect(host, port)

        return cls(conn)

    @classmethod
    def from_unix_socket(cls, path: Path) -> "Glue":
        """This establishes a connection to the server using a path that uses unix sockets.

        Args:
            path: A path that uses unix sockets.

        Returns:
            A "glue" object with a connection established from a unix socket.
        """
        conn = unix_connect(str(path))

        return cls(conn)

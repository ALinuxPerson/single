import attr
import typing as t
from pathlib import Path


@attr.s(auto_attribs=True, frozen=True)
class Version:
    major: int
    minor: int
    micro: int
    build: t.Optional[str]

    @classmethod
    def from_path(cls, path: Path) -> "Version":
        major = int((path / "major").read_text().strip())
        minor = int((path / "minor").read_text().strip())
        micro = int((path / "micro").read_text().strip())
        build = (path / "build").read_text().strip() or None

        return cls(major, minor, micro, build)

    def __str__(self) -> str:
        if self.build:
            return f"{self.major}.{self.minor}.{self.micro}.{self.build}"
        else:
            return f"{self.major}.{self.minor}.{self.micro}"


@attr.s(auto_attribs=True, frozen=True)
class CommandLine:
    help_message: str

    @classmethod
    def from_path(cls, path: Path) -> "CommandLine":
        help_message = path / "help_message"

        return cls(help_message.read_text())


@attr.s(auto_attribs=True, frozen=True)
class ClientCommandLine(CommandLine):
    pass


@attr.s(auto_attribs=True, frozen=True)
class ServerCommandLine(CommandLine):
    pass


@attr.s(auto_attribs=True, frozen=True)
class Client:
    command_line: ClientCommandLine

    @classmethod
    def from_path(cls, path: Path) -> "Client":
        command_line = ClientCommandLine.from_path(path / "command_line")

        return cls(command_line)  # type: ignore


@attr.s(auto_attribs=True, frozen=True)
class Server:
    command_line: ServerCommandLine

    @classmethod
    def from_path(cls, path: Path) -> "Server":
        command_line = ServerCommandLine.from_path(path / "command_line")

        return cls(command_line)  # type: ignore


@attr.s(auto_attribs=True, frozen=True)
class Theme:
    name: str
    description: str
    version: Version
    client: Client
    server: Server
    path: Path

    @classmethod
    def from_path(cls, path: Path) -> "Theme":
        name = ((path / "name").read_text()).strip()
        description = ((path / "description").read_text()).strip()
        version = Version.from_path(path / "version")
        client = Client.from_path(path / "client")
        server = Server.from_path(path / "server")

        return Theme(name, description, version, client, server, path)

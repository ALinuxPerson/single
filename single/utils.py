"""These are just some utility functions for single."""
import importlib
from pathlib import Path
from types import ModuleType
import importlib.util
import os
import typing as t
from single.enums import System
import platform
import attr


@attr.s(auto_attribs=True, frozen=True)
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


def get_module(path: Path) -> ModuleType:
    """This retrieves a module from a path.

    Args:
        path: The path of the module.

    Returns:
        The module.
    """
    if path.is_dir():
        raise IsADirectoryError("directories are not supported")

    module_name, _ = os.path.splitext(path.name)
    spec = importlib.util.spec_from_file_location(module_name, str(path))
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)  # type: ignore  # i don't care. if it works, it works.

    return module


def flatten_list(list_: t.List[t.Any]) -> t.List[t.Any]:
    """This flattens a list.

    Args:
        list_: The list to flatten.

    Examples:
        >>> nested_list = [[1, 2], [3, 4, 5], [6], [7, 8, 9, 10]]
        >>> flatten_list(nested_list)
        [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]

    Returns:
        The flattened list.
    """
    return [item for sub_list in list_ for item in sub_list]


def prettify_list(list_: t.List[t.Any]) -> str:
    """This prettifies a list by making it more human readable.

    Args:
        list_: The list to prettify.

    Examples:
        >>> things = ["shoebox", "horn", "mattress", 10]
        >>> prettify_list(things)
        'shoebox, horn, matress, 10'

    Returns:
        The prettified list.
    """
    return ", ".join([str(item) for item in list_])


def system() -> System:
    """This retrieves the current system os name as an enum.

    Returns:
        The system os name as an enum.
    """
    system_ = platform.system()
    return System(system_)

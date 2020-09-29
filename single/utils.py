import importlib
from pathlib import Path
from types import ModuleType
import importlib.util
import os
import typing as t


def get_module(path: Path) -> ModuleType:
    """This retrieves a module from a path.

    Args:
        path: The path of the module.

    Returns:
        The module.
    """
    module_name, _ = os.path.splitext(path.name)
    spec = importlib.util.spec_from_file_location(module_name, str(path))
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)  # type: ignore  # i don't care. if it works, it works.

    return module


def flatten_list(list_: t.List[t.Any]) -> t.List[t.Any]:
    """This flattens a list.

    Args:
        list_: The list to flatten.

    Returns:
        The flattened list.
    """
    return [item for sub_list in list_ for item in sub_list]


def prettify_list(list_: t.List[t.Any]) -> str:
    """This prettifies a list by making it more human readable.

    Args:
        list_: The list to prettify.

    Examples:
        >>> things = ["shoebox", "horn", "matress", 10]
        >>> prettify_list(things)
        'shoebox, horn, matress, 10'

    Returns:
        The prettified list.
    """
    return ", ".join([str(item) for item in list_])

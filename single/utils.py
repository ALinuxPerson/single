import importlib
from pathlib import Path
from types import ModuleType
import importlib.util
import os
import typing as t
from single._enums import System
from single import Flags
import platform


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
        >>> things = ["shoebox", "horn", "matress", 10]
        >>> prettify_list(things)
        'shoebox, horn, matress, 10'

    Returns:
        The prettified list.
    """
    return ", ".join([str(item) for item in list_])


def parse_system_flag(flag: Flags) -> System:
    """This parses a singular flag to its System enum equivalent.

    Args:
        flag: The flag to parse.

    Raises:
        ValueError: if the wrong flags was given e.g. any flag that isn't {LINUX,MAC,WINDOWS,BSD}_SUPPORTED

    Returns:
        The parsed flag.
    """
    flag_system_map = {
        Flags.LINUX_SUPPORTED: System.LINUX,
        Flags.MAC_SUPPORTED: System.MAC,
        Flags.WINDOWS_SUPPORTED: System.WINDOWS,
        Flags.BSD_SUPPORTED: System.BSD,
    }

    try:
        return flag_system_map[flag]
    except KeyError:
        raise ValueError(
            f"flag '{flag}' is not valid for this scenario; use Flags.{{LINUX,MAC,WINDOWS,BSD}}_SUPPORTED instead"
        ) from None


def get_compatible_systems(*flags: Flags) -> t.List[System]:
    """This retrieves a list of systems supported from flags.

    Args:
        *flags: The flags, usually from Source.FLAGS

    Returns:
        A list of systems supported.
    """
    OS_SUPPORTED = [
        Flags.WINDOWS_SUPPORTED,
        Flags.LINUX_SUPPORTED,
        Flags.MAC_SUPPORTED,
        Flags.BSD_SUPPORTED,
    ]
    compatible_systems: t.List[System] = []

    for flag in flags:
        if flag in OS_SUPPORTED:
            parsed_flag = parse_system_flag(flag)
            compatible_systems.append(parsed_flag)
        elif flag == Flags.ALL_OS_SUPPORTED:
            compatible_systems.clear()
            compatible_systems.extend(
                parse_system_flag(unparsed_flag) for unparsed_flag in OS_SUPPORTED
            )
            break

    return compatible_systems


def get_system() -> System:
    """This retrieves the current system os name as an enum.

    Returns:
        The system os name as an enum.
    """
    system = platform.system()
    return System(system)

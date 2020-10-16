from single import utils
from single import Flag
from pathlib import Path
from single.enums import System
import platform
import pytest

file = Path(__file__)
current_dir = file.parent


def test_server_state_from_errors() -> None:
    errors = [ValueError(), RuntimeError()]
    server_state_no_errs = utils.ServerState.from_errors([])
    server_state_with_errs = utils.ServerState.from_errors(errors)

    assert server_state_no_errs.ok
    assert not server_state_with_errs.ok
    assert not server_state_no_errs.errors
    assert server_state_with_errs.errors == errors


def test_get_module() -> None:
    utils_module = utils.get_module(current_dir.parent / "single" / "utils.py")

    assert utils_module.get_system() == utils.get_system()  # type: ignore


def test_get_module_directory() -> None:
    with pytest.raises(IsADirectoryError):
        utils.get_module(current_dir.parent / "single")


def test_flatten_list() -> None:
    nested_list = [[1, 2], [3, 4, 5], [6], [7, 8, 9, 10]]
    flattened_list = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]

    assert utils.flatten_list(nested_list) == flattened_list


def test_prettify_list() -> None:
    unprettified_list = ["shoebox", "horn", "mattress", 10]
    prettified_list = "shoebox, horn, mattress, 10"

    assert utils.prettify_list(unprettified_list) == prettified_list


def test_parse_system_flag() -> None:
    assert utils.parse_system_flag(Flag.LINUX_SUPPORTED) == System.LINUX
    assert utils.parse_system_flag(Flag.WINDOWS_SUPPORTED) == System.WINDOWS
    assert utils.parse_system_flag(Flag.MAC_SUPPORTED) == System.MAC
    assert utils.parse_system_flag(Flag.BSD_SUPPORTED) == System.BSD

    with pytest.raises(ValueError):
        utils.parse_system_flag(Flag.DOWNGRADE_SUPPORTED)


def test_get_compatible_systems() -> None:
    os_supported = [System.WINDOWS, System.LINUX, System.MAC, System.BSD]
    assert utils.get_compatible_systems(Flag.LINUX_SUPPORTED, Flag.BSD_SUPPORTED) == [
        System.LINUX,
        System.BSD,
    ]
    assert utils.get_compatible_systems(Flag.ALL_OS_SUPPORTED) == os_supported


def test_get_system() -> None:
    system = platform.system()
    system_enum = utils.get_system()

    if system == "Linux":
        assert system_enum == System.LINUX
    elif system == "Windows":
        assert system_enum == System.WINDOWS
    elif system == "Darwin":
        assert system_enum == System.MAC
    elif system == "FreeBSD":
        assert system_enum == System.BSD

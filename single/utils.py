import importlib
from pathlib import Path
from types import ModuleType
import importlib.util
import os


def get_module(path: Path) -> ModuleType:
    """This retrieves a module from a path.

    Args:
        path: The path of the module.

    Returns:
        The module.
    """
    module_name: str
    module_name, _ = os.path.splitext(path.name)
    spec = importlib.util.spec_from_file_location(module_name, str(path))
    module: ModuleType = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)  # type: ignore  # i don't care. if it works, it works.

    return module

"""These contain some common constants for single."""
import appdirs  # type: ignore
from single import __version__ as version
from pathlib import Path

APP_NAME: str = "single"
AUTHOR: str = "ALinuxPerson"
_appdirs: appdirs.AppDirs = appdirs.AppDirs(APP_NAME, AUTHOR, version)
USER_DATA_DIR: Path = Path(_appdirs.user_data_dir())
USER_SOURCES_DIR: Path = USER_DATA_DIR / "sources"
GLOBAL_SOURCES_DIR: Path = Path(__file__) / "sources"

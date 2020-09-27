"""These contain some common constants for single."""
import appdirs  # type: ignore
from pathlib import Path
import typing as t

APP_NAME: str = "single"
AUTHOR: str = "ALinuxPerson"
_appdirs: appdirs.AppDirs = appdirs.AppDirs(APP_NAME, AUTHOR)
USER_DATA_DIR: Path = Path(_appdirs.user_data_dir)
USER_SOURCES_DIR: Path = USER_DATA_DIR / "sources"
GLOBAL_SOURCES_DIR: Path = Path(__file__).parent / "sources"
SOURCES_DIRS: t.List[Path] = [GLOBAL_SOURCES_DIR, USER_SOURCES_DIR]

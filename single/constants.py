"""These contain some common constants for single."""
import appdirs  # type: ignore
from pathlib import Path

APP_NAME = "single"
AUTHOR = "ALinuxPerson"
_appdirs = appdirs.AppDirs(APP_NAME, AUTHOR)
USER_DATA_DIR = Path(_appdirs.user_data_dir)
USER_SOURCES_DIR = USER_DATA_DIR / "sources"
GLOBAL_SOURCES_DIR = Path(__file__).parent / "sources"
SOURCES_DIRS = [GLOBAL_SOURCES_DIR, USER_SOURCES_DIR]
POSSIBLE_LOGGING_LEVELS = ["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"]

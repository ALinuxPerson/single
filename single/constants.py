"""These contain some common constants for single."""
import appdirs  # type: ignore
from pathlib import Path

APP_NAME = "single"
AUTHOR = "ALinuxPerson"
_appdirs = appdirs.AppDirs(APP_NAME, AUTHOR)
USER_DATA_DIR = Path(_appdirs.user_data_dir)
USER_PROVIDERS_DIR = USER_DATA_DIR / "providers"
GLOBAL_PROVIDERS_DIR = Path(__file__).parent / "providers"
PROVIDERS_DIRS = [GLOBAL_PROVIDERS_DIR, USER_PROVIDERS_DIR]
POSSIBLE_LOGGING_LEVELS = ["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"]

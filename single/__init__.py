"""These contain the most common imports a developer would have and the version number for single."""
from single.models import Package, Source
from single.enums import Flags
from single.exceptions import UnsupportedSystemError
from single.core import process_flags

__version__ = "0.1.0"

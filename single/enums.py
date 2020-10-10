"""This contains some flags mainly used in sources."""
import enum as e


class Flag(e.Enum):
    """Flags that your custom source can use."""

    PARTIAL_UPGRADES_SUPPORTED = e.auto()
    ALL_OS_SUPPORTED = e.auto()
    WINDOWS_SUPPORTED = e.auto()
    MAC_SUPPORTED = e.auto()
    LINUX_SUPPORTED = e.auto()
    BSD_SUPPORTED = e.auto()
    DOWNGRADE_SUPPORTED = e.auto()


class LoggingLevel(e.Enum):
    TRACE = "TRACE"
    DEBUG = "DEBUG"
    INFO = "INFO"
    WARNING = "WARNING"
    ERROR = "ERROR"
    CRITICAL = "CRITICAL"
    SUCCESS = "SUCCESS"

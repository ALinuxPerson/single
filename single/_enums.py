"""These are some private enums that have no business being publicly accessible to the developer."""
import enum as e


class System(e.Enum):
    WINDOWS = "Windows"
    MAC = "Darwin"
    LINUX = "Linux"
    BSD = "FreeBSD"


class LoggingLevel(e.Enum):
    TRACE = "TRACE"
    DEBUG = "DEBUG"
    INFO = "INFO"
    WARNING = "WARNING"
    ERROR = "ERROR"
    CRITICAL = "CRITICAL"
    SUCCESS = "SUCCESS"

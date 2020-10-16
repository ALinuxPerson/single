"""These are some private enums that have no business being publicly accessible to the developer."""
import enum as e


class LoggingLevel(e.Enum):
    """This is a less error prone way of getting the logging level."""

    TRACE = "TRACE"
    DEBUG = "DEBUG"
    INFO = "INFO"
    WARNING = "WARNING"
    ERROR = "ERROR"
    CRITICAL = "CRITICAL"
    SUCCESS = "SUCCESS"

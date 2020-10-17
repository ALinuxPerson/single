"""This contains some flags mainly used in sources."""
import enum as e


class System(e.Enum):
    """This is a less error prone way of getting the system os name."""

    WINDOWS = "Windows"
    MAC = "Darwin"
    LINUX = "Linux"
    BSD = "FreeBSD"

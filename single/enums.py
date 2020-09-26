import enum as e


class Flags(e.Enum):
    """Flags that your custom source can use."""

    PARTIAL_UPGRADES_SUPPORTED = e.auto()
    ALL_OS_SUPPORTED = e.auto()
    WINDOWS_SUPPORTED = e.auto()
    MAC_SUPPORTED = e.auto()
    LINUX_SUPPORTED = e.auto()
    BSD_SUPPORTED = e.auto()
    DOWNGRADE_SUPPORTED = e.auto()

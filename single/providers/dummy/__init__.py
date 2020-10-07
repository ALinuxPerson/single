from single import Source, Flag, Package, UnsupportedSystemError, process_flags
import typing as t


class DummySource(Source):
    @property
    def FLAGS(self) -> t.List[Flag]:
        return [
            Flag.ALL_OS_SUPPORTED,
            Flag.DOWNGRADE_SUPPORTED,
            Flag.PARTIAL_UPGRADES_SUPPORTED,
        ]

    @property
    def backend_version(self) -> str:
        return "0.1.0"

    def supported(self) -> None:
        process_flags(self.__class__.__name__, *self.FLAGS)
        raise UnsupportedSystemError(
            "The system doesn't have the appropriate libraries installed.",
            "Install libraries 'libalpm', 'libapt' and 'libpython'.",
        )

    def package(self, name: str) -> t.List[Package]:
        return [Package("dummy", "0.1.0", "This is a dummy package.", 2.0, 1.0)]

    def install_package(self, *packages: Package) -> None:
        pass

    def remove_package(self, *packages: Package) -> None:
        pass

    def update_package(self, *packages: Package) -> None:
        pass

    def greet(self) -> None:
        self.context.info(
            f"Dummy Source Version 0.1.1\n\n" f"This is a dummy provider."
        )

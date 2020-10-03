from single import Source, Flags, Package, UnsupportedSystemError
import typing as t


class DummySource(Source):
    @property
    def FLAGS(self) -> t.List[Flags]:
        return [
            Flags.ALL_OS_SUPPORTED,
            Flags.DOWNGRADE_SUPPORTED,
            Flags.PARTIAL_UPGRADES_SUPPORTED,
        ]

    @property
    def backend_version(self) -> str:
        return "0.1.0"

    def supported(self) -> None:
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

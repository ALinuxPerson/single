from single import Source, Package, UnsupportedSystemError, System
import typing as t


class DummySource(Source):
    os_supported = [System.MAC, System.WINDOWS, System.BSD]

    @property
    def backend_version(self) -> str:
        return "0.1.0"

    def supported(self) -> None:
        super().supported()
        raise UnsupportedSystemError(
            "a",
            "",
        )

    def package(self, name: str) -> t.List[Package]:
        return [Package("dummy", "0.1.0", "This is a dummy package.", 2.0, 1.0, self)]

    def install_package(self, *packages: Package) -> None:
        pass

    def remove_package(self, *packages: Package) -> None:
        pass

    def update_package(self, *packages: Package) -> None:
        pass

    def greet(self) -> None:
        self.context.success(
            f"Dummy Source Version 0.1.1\n" f"This is a dummy provider."
        )

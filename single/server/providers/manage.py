from single import Source, Package, System, __version__ as single_version
import attr
import typing as t


@attr.s(auto_attribs=True, frozen=True)
class SinglePackage(Package):
    other: t.Dict[str, t.Any] = {}


@attr.s(auto_attribs=True)
class SingleSource(Source):
    # this supposedly was a positional argument, and it still 'is', but the context argument has a default, and since
    # python errors me out if i have a positional argument after a default argument, we're gonna have to make a fake
    # default argument for sources and if the user doesn't give out any sources just raise an exception saying
    # you need to fill the sources out. i know, it's a hack.
    sources: t.List[Source] = []

    def _package_to_single_package(self, package: Package) -> SinglePackage:
        """This converts a regular package from any other provider to one that can be usable.

        Args:
            package: The package to convert.

        Returns:
            The converted package.
        """

    def _packages_to_single_packages(self, packages: Package) -> t.List[SinglePackage]:
        """Iterable version of self._package_to_single_package.

        Args:
            *packages: The packages to convert.

        Returns:
            The converted packages.
        """

    @property
    def os_supported(self) -> t.List[System]:
        return [System.LINUX, System.WINDOWS, System.MAC, System.BSD]

    @property
    def backend_version(self) -> str:
        return single_version

    def supported(self) -> None:
        super().supported()

    def package(self, name: str) -> t.List[SinglePackage]:  # type: ignore
        packages: t.List[SinglePackage] = []

        for source in self.sources:
            converted_packages = self._packages_to_single_packages(
                *source.package(name)
            )
            packages.extend(converted_packages)

        return packages

    def install_package(self, *packages: Package) -> None:
        for package in packages:
            source = package.original_source
            source.install_package(package)

    def remove_package(self, *packages: Package) -> None:
        for package in packages:
            source = package.original_source
            source.remove_package(package)

    def update_package(self, *packages: Package) -> None:
        for package in packages:
            source = package.original_source
            source.update_package(package)

    def greet(self) -> None:
        self.context.success(
            f"The Single Source (One Source) System Ready and Initialized.\n"
            f"Backend Version {self.backend_version}"
        )

    def __attrs_post_init__(self) -> None:
        # yeah...
        if not self.sources:
            raise TypeError(
                "__init__() missing 1 required positional argument: 'sources' (do sources=[...])"
            )

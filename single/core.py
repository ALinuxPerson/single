"""This provides some core classes and functions for `single`."""
import attr
from single import Package, Source, UnsupportedSystemError
from single import utils as u
import typing as t
from pathlib import Path
import toml


@attr.s(auto_attribs=True, frozen=True)
class ProviderMetadata:
    """This contains metadata that should've been provided by the provider from provider.toml.

    Args:
        name: The name of the provider.
        version: The version of the provider.
        description: The description of the provider.
        source_reference: The raw, uninitialized source class.
        package_reference: The raw, uninitialized package class.
        dependencies: The python dependencies the provider needs.
    """

    name: str
    version: str
    description: str
    source_reference: t.Type[Source]
    package_reference: t.Type[Package]
    dependencies: t.List[str]

    @classmethod
    def from_provider(cls, provider_path: Path) -> "ProviderMetadata":
        """This gets ProviderMetadata from a provider folder.

        Args:
            provider_path: The provider path.

        Raises:
            FileNotFoundError: If the provider path doesn't exist
            NotADirectoryError: If the provider path isn't a directory.

        Returns:
            The provider metadata.
        """
        if not provider_path.exists():
            raise FileNotFoundError(f"provider path '{provider_path}' doesn't exist")
        if not provider_path.is_dir():
            raise NotADirectoryError(
                f"provider path '{provider_path}' must be a directory"
            )

        metadata_path = provider_path / "provider.toml"
        metadata = toml.loads(metadata_path.read_text())["metadata"]
        module = u.get_module(provider_path / "__init__.py")
        source_ref = getattr(module, metadata["source_name"])
        package_ref = getattr(module, metadata["package_name"])
        return cls(
            metadata["name"],
            metadata["version"],
            metadata["description"],
            source_ref,
            package_ref,
            metadata["dependencies"],
        )

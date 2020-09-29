import attr
from single import Package, Source
from single import utils as u
import typing as t
from pathlib import Path
import toml


@attr.s(auto_attribs=True, frozen=True)
class SourceMetadata:
    name: str
    version: str
    description: str
    source_reference: t.Type[Source]
    package_reference: t.Type[Package]
    dependencies: t.List[str]

    @classmethod
    def from_source(cls, source_path: Path) -> "SourceMetadata":
        """This gets SourceMetadata from a source folder.

        Args:
            source_path: The source path.

        Returns:
            The source metadata.
        """
        if not source_path.exists():
            raise FileNotFoundError(f"source path '{source_path}' doesn't exist")
        if not source_path.is_dir():
            raise NotADirectoryError(f"source path '{source_path}' must be a directory")

        metadata_path = source_path / "source.toml"
        metadata = toml.loads(metadata_path.read_text())["metadata"]  # type: ignore
        module = u.get_module(source_path / "__init__.py")
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

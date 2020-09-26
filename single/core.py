from types import ModuleType
import attr
from single import Package, Source
import typing as t
from pathlib import Path
import toml
from single import utils as u


@attr.s(auto_attribs=True, frozen=True)
class SourceMetadata:
    name: str
    version: str
    description: str
    source_reference: Source
    package_reference: Package
    dependencies: t.List[str]

    @classmethod
    def from_source(cls, source_path: Path) -> "SourceMetadata":
        """This gets SourceMetadata from a source folder.

        Args:
            source_path: The source path.

        Returns:
            The source metadata.
        """
        if not source_path.is_dir():
            raise NotADirectoryError("source path must be a directory")
        metadata_path: Path = source_path / "source.toml"
        metadata: t.Dict[str, t.Any] = toml.loads(metadata_path.read_text())["metadata"]  # type: ignore
        module: ModuleType = u.get_module(source_path / "__init__.py")
        source_ref: Source = getattr(module, metadata["source_name"])
        package_ref: Package = getattr(module, metadata["package_name"])
        return cls(
            metadata["name"],
            metadata["version"],
            metadata["description"],
            source_ref,
            package_ref,
            metadata["dependencies"],
        )

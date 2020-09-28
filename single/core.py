import attr
from single import Package, Source
from single import utils as u
import typing as t
from pathlib import Path
import toml
from single.constants import SOURCES_DIRS


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

    def __attrs_post_init__(self) -> None:
        return self.source_reference.supported()


def find_sources(dirs: t.List[Path] = None) -> t.List[Path]:
    """This finds sources from directories.

    Args:
        dirs: The directories.

    Returns:
        A list of paths which could be sources.
    """
    dirs = dirs or SOURCES_DIRS
    dirs_iterdir = [dir_.iterdir() for dir_ in dirs]
    all_paths = u.flatten_list(dirs_iterdir)
    return [path for path in all_paths if path.is_dir()]


def get_sources(dirs: t.List[Path] = None) -> t.List[SourceMetadata]:
    """This gets sources from multiple directories.

    Args:
        dirs: The directories to get sources from.

    Returns:
        A list of Source Metadata.
    """
    dirs = dirs or SOURCES_DIRS
    sources_found = find_sources(dirs)
    return [SourceMetadata.from_source(dir_) for dir_ in sources_found]

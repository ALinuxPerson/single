from single import core, Source, Package
from pathlib import Path
import platform
import pytest


current_folder = Path(__file__).parent


def test_that_provider_metadata_raises_a_file_not_found_error_on_a_nonexistent_provider() -> None:
    nonexistent_provider = current_folder / "i-do-not-exist"
    with pytest.raises(FileNotFoundError):
        core.ProviderMetadata.from_provider(nonexistent_provider)


def test_that_provider_metadata_raises_a_not_a_directory_error_on_a_provider_being_a_file() -> None:
    provider_file = current_folder / "providers" / "provider-file"
    with pytest.raises(NotADirectoryError):
        core.ProviderMetadata.from_provider(provider_file)


def test_that_provider_metadata_processes_a_provider_folder_correctly() -> None:
    provider_folder = current_folder / "providers" / "test"
    provider_metadata = core.ProviderMetadata.from_provider(provider_folder)

    assert provider_metadata.name == "Test Provider"
    assert provider_metadata.version == "0.1.0"
    assert provider_metadata.description == "Testing Provider."
    assert provider_metadata.source_reference == Source
    assert provider_metadata.package_reference == Package
    assert provider_metadata.dependencies == []

from single.server.utils import ml_error
from pathlib import Path
from single.core import ProviderMetadata
from single import UnsupportedSystemError


def preprocess_provider_error(error: str, provider_dir: Path) -> None:
    """This is a shortcut for printing out a pre-processing provider error.

    Args:
        error: The error.
        provider_dir: The provider directory since the ProviderMetadata can't be initialized at this point.

    Returns:
        Nothing.
    """
    ml_error(
        "During initialization of a provider:\n"
        f"A provider has encountered an error (path is {provider_dir})\n"
        f"{error}"
    )


def postprocess_provider_error(
    provider: "ProviderMetadata", error: UnsupportedSystemError
) -> UnsupportedSystemError:
    ml_error(
        f"During source checks:\n"
        f"The provider '{provider.name}' has encountered a fatal error:\n"
        f"From source '{provider.source_reference().__class__.__name__}':\n"
        f"{error.message}\n\n"
        f"These are the actions that need to be done:\n"
        f"{error.action_needed}"
    )
    return error

from single.core import ProviderMetadata
from pathlib import Path
from single.server.providers.errors import (
    preprocess_provider_error,
    postprocess_provider_error,
)
from loguru import logger
from toml.decoder import TomlDecodeError
from single.context import Context
from single import UnsupportedSystemError
import typing as t


def preprocess_provider(
    provider_dir: Path,
) -> t.Union[ProviderMetadata, Exception]:
    """This brings the provider to the pre-processing phase.

    The pre processing phase tries to get provider metadata from a provider folder. This phase
    will fail if an error occurs while trying to get the provider metadata.

    Args:
        provider_dir: The provider directory.

    Returns:
        Provider metadata if nothing go
    """
    logger.debug(f"Pre-processing provider (path is '{provider_dir}')")
    try:
        return ProviderMetadata.from_provider(provider_dir)
    except FileNotFoundError as error:
        preprocess_provider_error(f"A certain file wasn't found: {error}", provider_dir)
        return error
    except AttributeError as error:
        preprocess_provider_error(
            f"A source reference or a package reference is missing: {error}",
            provider_dir,
        )
        return error
    except TomlDecodeError as error:
        preprocess_provider_error(
            f"The provider configuration couldn't be read properly: {error}",
            provider_dir,
        )
        return error


def postprocess_provider(provider: ProviderMetadata, context: Context) -> None:
    """This brings a provider to the post-processing phase.

    The post-processing phase tests the source reference grabbed from the provider metadata
    if it's supported or not. This is also the phase where we'll know whether a provider
    is fit to be added to a provider list.

    Args:
        provider: The provider metadata.
        context: The context.

    Returns:
        Nothing.
    """
    logger.debug(f"Post-processing provider '{provider.name}'")
    # noinspection PyArgumentList
    source_reference = provider.source_reference(context)  # some bug happened

    try:
        source_reference.supported()
    except UnsupportedSystemError as error:
        raise postprocess_provider_error(provider, error)

    logger.debug("Now greeting server")
    source_reference.greet()

    return None

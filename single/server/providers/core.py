import typing as t
from pathlib import Path
from loguru import logger
from single.constants import PROVIDERS_DIRS
from single import utils
from single.core import ProviderMetadata
from single.exceptions import UnsupportedSystemError
from single.context import Context, ServerContext
from single.server.providers.processing import preprocess_provider, postprocess_provider


def load_providers(
    provider_list: t.List[ProviderMetadata], errors_list: t.List[Exception]
) -> None:
    """This loads all providers from all found providers in get_providers.

    Args:
        provider_list: The provider list.
        errors_list: The error list.

    Returns:
        Nothing.
    """
    logger.info("Loading the providers....")

    providers, errors = get_providers()
    provider_list.extend(providers)
    logger.trace(
        f"Provider list after merge with providers from get_providers(): {provider_list}"
    )
    errors_list.extend(errors)
    logger.trace(
        f"Error list after merge with errors from get_providers(): {errors_list}"
    )


def find_providers(dirs: t.List[Path] = None) -> t.List[Path]:
    """This finds providers from directories.

    Args:
        dirs: The directories.

    Returns:
        A list of paths which could be providers.
    """
    logger.debug("Finding providers...")
    logger.trace(f"find_providers(dirs={dirs})")
    dirs = dirs or PROVIDERS_DIRS
    logger.trace(f"Directories after processing: {dirs}")
    logger.debug(f"Directories chosen: {utils.prettify_list(dirs)}")
    logger.trace(f"Entering for loop to check whether or not directories exist")
    for dir_ in dirs:
        logger.trace(f"Current directory: {dir_}")
        if not dir_.exists():
            logger.debug(f"Directory {dir_} doesn't exist, continuing.")
            dirs.remove(dir_)
    dirs_iterdir = [dir_.iterdir() for dir_ in dirs]
    logger.trace(f"All accepted directories after exist check: {dirs_iterdir}")
    all_paths = utils.flatten_list(dirs_iterdir)
    logger.trace(f"Flattened accepted directories: {all_paths}")
    return [path for path in all_paths if path.is_dir()]


def get_providers(
    dirs: t.List[Path] = None,
) -> t.Tuple[t.List[ProviderMetadata], t.List[Exception]]:
    """This gets all providers from a provider directory (or optionally specified) and put them in a
    series of few tests to determine whether they're fit to be added to a provider list or not.

    Args:
        dirs: The provider directories.

    Returns:
        A list of provider metadata and a list of all exceptions gathered.
    """
    logger.trace(f"get_providers(dirs={dirs})")
    dirs = dirs or PROVIDERS_DIRS
    logger.trace(f"Directories after processing: {dirs}")
    possible_providers = find_providers(dirs)
    logger.trace(f"Possible providers: {possible_providers}")
    provider_metadata: t.List[ProviderMetadata] = []
    errors: t.List[Exception] = []
    context: Context = ServerContext(logger)

    logger.trace(
        "Now iterating through all providers to see if each are fit to be used"
    )
    for provider in possible_providers:
        logger.trace(f"Current provider: {provider}")
        preprocessed_provider = preprocess_provider(provider)
        logger.trace(f"Pre-processed provider: {preprocessed_provider}")
        if isinstance(preprocessed_provider, Exception):
            errors.append(preprocessed_provider)
            continue

        try:
            postprocess_provider(preprocessed_provider, context)
        except UnsupportedSystemError as error:
            errors.append(error)
            continue

        logger.success(f"Loaded provider '{preprocessed_provider.name}'")
        provider_metadata.append(preprocessed_provider)

    logger.trace(
        f"After for loop: provider_metadata={provider_metadata}, errors={errors}"
    )
    logger.info(
        f"{len(provider_metadata)}/{len(possible_providers)} provider(s) loaded"
    )

    return provider_metadata, errors

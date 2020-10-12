"""These are just some utilities used by the single server."""
from single import _enums as enums
from single.core import ProviderMetadata
from single.constants import PROVIDERS_DIRS
from toml.decoder import TomlDecodeError  # type: ignore
from single import UnsupportedSystemError, utils
from single.context import Context
from single.context import ServerContext
from pathlib import Path
import loguru as log
import typing as t
import sys

# noinspection PyTypeChecker
logger: "log.Logger" = None  # type: ignore  # will be initialized later


def initialize_logger(logger_: "log.Logger") -> None:
    """This initializes the logger.

    Args:
        logger_: The logger.

    Returns:
        Nothing.
    """
    global logger

    logger = logger_


def set_logging_level(logging_level: enums.LoggingLevel) -> None:
    """This sets the logging level without the use of an environment variable.

    Args:
        logging_level: The logging level.

    Returns:
        Nothing.
    """
    logger.remove()
    logger.add(sys.stderr, level=logging_level.value)


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


def ml_error(*message: str) -> None:
    """This prints out a multi line error message.

    Args:
        *message: The message.

    Returns:
        Nothing.
    """
    combined_msg = " ".join(message)

    for line in combined_msg.splitlines():
        logger.error(line)


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


def postprocess_provider(
    provider: ProviderMetadata, context: Context
) -> t.Optional[UnsupportedSystemError]:
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
        ml_error(
            f"During source checks:\n"
            f"The provider '{provider.name}' has encountered a fatal error:\n"
            f"From source '{provider.source_reference().__class__.__name__}':\n"
            f"{error.message}\n\n"
            f"These are the actions that need to be done:\n"
            f"{error.action_needed}"
        )
        return error

    logger.debug("Now greeting server")
    source_reference.greet()

    return None


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
        postprocessed_provider = postprocess_provider(preprocessed_provider, context)
        if postprocessed_provider:
            errors.append(postprocessed_provider)
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

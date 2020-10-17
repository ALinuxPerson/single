"""These are some exceptions that should be raised by sources."""


class SingleError(Exception):
    """This is a generic error for single sources."""

    @property
    def message(self) -> str:
        """The message.

        Returns:
            The message.
        """
        return self.args[0]

    @property
    def action_needed(self) -> str:
        """The actions needed for a source to work.

        Returns:
            The actions needed for a source to work.
        """
        return self.args[1]


class UnsupportedSystemError(SingleError):
    """This is an error that should be raised on Source.supported if checks fail."""

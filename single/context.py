import attr


@attr.s(auto_attribs=True)
class Context:
    """This is the context system.

    The context system is a way for sources, servers and clients to "speak" with each other.
    This is also an argument for sources now.
    This is the theoretical path ways for speaking:
    Source -> Server -> Client
    Source -> Client
    Source -> Server
    There is only one way communication as of now.

    There are 3 planned contexts:

    VoidContext:
        This is just a placeholder context that doesn't output a message. This is useful if you only want to
        interact with the sources directly without any daemon or client interference.

    ServerContext:
        This is a way for the sources to directly log a message to the server. This can be used as a "welcome"
        when a source is loaded, for example.

    ClientContext:
        This is a way for the sources to directly log a message to the server. Of course, the server still
        needs to intercept the logging messages for this to work, maybe put an 'context' argument to
        {install,remove,update}_packages, maybe?
    """

    def trace(self, *message: str) -> None:
        """Print a trace message.

        Args:
            *message: The message.

        Returns:
            Nothing.
        """
        raise NotImplementedError

    def debug(self, *message: str) -> None:
        """Print a debug message.

        Args:
            *message: The message.

        Returns:
            Nothing.
        """
        raise NotImplementedError

    def info(self, *message: str) -> None:
        """Print an info message.

        Args:
            *message: The message.

        Returns:
            Nothing.
        """
        raise NotImplementedError

    def warn(self, *message: str) -> None:
        """Print a warning message.

        Args:
            *message: The message.

        Returns:
            Nothing.
        """
        raise NotImplementedError

    def success(self, *message: str) -> None:
        """Print a success message.

        Args:
            *message: The message.

        Returns:
            Nothing.
        """
        raise NotImplementedError

    def error(self, *message: str) -> None:
        """Print an error message.

        Args:
            *message: The message.

        Returns:
            Nothing.
        """
        raise NotImplementedError

    def critical(self, *message: str) -> None:
        """Print a critical message.

        Args:
            *message: The message.

        Returns:
            Nothing.
        """
        raise NotImplementedError


@attr.s(auto_attribs=True)
class VoidContext(Context):
    """This is a void context.

    This is a context where nothing gets printed out. It is intended to be used for direct access to sources.
    For example, interacting with a source directly through the Python interpreter.
    """

    def trace(self, *message: str) -> None:
        pass

    def debug(self, *message: str) -> None:
        pass

    def info(self, *message: str) -> None:
        pass

    def warn(self, *message: str) -> None:
        pass

    def error(self, *message: str) -> None:
        pass

    def critical(self, *message: str) -> None:
        pass

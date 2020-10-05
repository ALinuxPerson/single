from single.models import Context
import attr


@attr.s(auto_attribs=True)
class VoidContext(Context):
    """This is a void context.

    This is a context where nothing gets printed out. It is intended to be used for direct access to sources.
    For example, interacting with a source directly through the Python interpreter.
    """

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

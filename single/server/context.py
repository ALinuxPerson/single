from single.context import Context
import loguru as log
import attr


@attr.s(auto_attribs=True)
class ServerContext(Context):
    logger: "log.Logger"

    def trace(self, *message: str) -> None:
        combined_message = " ".join(message)

        for line in combined_message.splitlines():
            self.logger.trace(line)

    def debug(self, *message: str) -> None:
        combined_message = " ".join(message)

        for line in combined_message.splitlines():
            self.logger.debug(line)

    def info(self, *message: str) -> None:
        combined_message = " ".join(message)

        for line in combined_message.splitlines():
            self.logger.info(line)

    def warn(self, *message: str) -> None:
        combined_message = " ".join(message)

        for line in combined_message.splitlines():
            self.logger.warning(line)

    def error(self, *message: str) -> None:
        combined_message = " ".join(message)

        for line in combined_message.splitlines():
            self.logger.error(line)

    def critical(self, *message: str) -> None:
        combined_message = " ".join(message)

        for line in combined_message.splitlines():
            self.logger.critical(line)

    def success(self, *message: str) -> None:
        combined_message = " ".join(message)

        for line in combined_message.splitlines():
            self.logger.success(line)

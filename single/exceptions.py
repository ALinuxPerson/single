class UnsupportedSystemError(Exception):
    @property
    def message(self) -> str:
        return self.args[0]

    @property
    def action_needed(self) -> str:
        return self.args[1]

from single import UnsupportedSystemError


def test_unsupported_system_error() -> None:
    try:
        raise UnsupportedSystemError("Hello World", "World Hello")
    except UnsupportedSystemError as error:
        assert error.message == "Hello World"
        assert error.action_needed == "World Hello"

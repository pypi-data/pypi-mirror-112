"""This modules contains custom Myst exceptions."""


class BaseMystError(Exception):
    """Base class for any exceptions raised in this library."""

    pass


class MystClientError(BaseMystError):
    """Generic errors in the Myst client."""

    pass


class UnAuthenticatedError(BaseMystError):
    """Raised when authentication is missing or fails."""

    def __init__(self, message):
        """An `UnAuthenticatedError` is initialized with a message."""
        super().__init__(message)
        self.message = message


class MystAPIError(BaseMystError):
    """Generic Myst API error."""

    def __init__(self, status_code, message):
        """A `MystAPIError` is initialized with an HTTP status code and a message."""
        super().__init__(message)
        self.status_code = status_code
        self.message = message

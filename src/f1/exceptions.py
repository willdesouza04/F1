"""Custom exceptions for the F1 library."""


class OpenF1Error(Exception):
    """Base exception for all F1 library errors."""

    pass


class NetworkError(OpenF1Error):
    """Raised when there is a network/connection error."""

    pass


class APIError(OpenF1Error):
    """Raised when the API returns an error (4xx/5xx)."""

    pass


class NotFoundError(APIError):
    """Raised when a resource is not found (404)."""

    pass

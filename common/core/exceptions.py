"""Shared custom exceptions."""


class AppException(Exception):
    """Base application exception."""

    def __init__(self, message: str, status_code: int = 500) -> None:
        self.message = message
        self.status_code = status_code
        super().__init__(message)


class NotFoundException(AppException):
    """Raised when a requested resource is not found."""

    def __init__(self, message: str = "Resource not found") -> None:
        super().__init__(message, status_code=404)


class ValidationException(AppException):
    """Raised when input validation fails."""

    def __init__(self, message: str = "Validation error") -> None:
        super().__init__(message, status_code=422)


class AuthException(AppException):
    """Raised for authentication/authorization failures."""

    def __init__(self, message: str = "Authentication failed") -> None:
        super().__init__(message, status_code=401)


class ConflictException(AppException):
    """Raised when a resource conflict occurs."""

    def __init__(self, message: str = "Resource conflict") -> None:
        super().__init__(message, status_code=409)

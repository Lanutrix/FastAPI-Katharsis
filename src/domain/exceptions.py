"""Domain-level exceptions."""


class DomainException(Exception):
    """Base exception for domain errors."""

    def __init__(self, message: str = "A domain error occurred"):
        self.message = message
        super().__init__(self.message)


class UserAlreadyExistsError(DomainException):
    """Raised when attempting to create a user that already exists."""

    def __init__(self, email: str):
        super().__init__(f"User with email '{email}' already exists")


class UserNotFoundError(DomainException):
    """Raised when a user is not found."""

    def __init__(self, identifier: str):
        super().__init__(f"User not found: {identifier}")


class InvalidCredentialsError(DomainException):
    """Raised when authentication credentials are invalid."""

    def __init__(self):
        super().__init__("Invalid email or password")


class InvalidTokenError(DomainException):
    """Raised when a token is invalid or expired."""

    def __init__(self, message: str = "Invalid or expired token"):
        super().__init__(message)


class MathOperationError(DomainException):
    """Raised when a math operation fails."""

    def __init__(self, message: str):
        super().__init__(message)


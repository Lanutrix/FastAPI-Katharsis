"""Password hasher interface."""

from abc import ABC, abstractmethod


class IPasswordHasher(ABC):
    """Abstract interface for password hashing operations."""

    @abstractmethod
    def hash(self, password: str) -> str:
        """
        Hash a plain text password.

        Args:
            password: Plain text password

        Returns:
            Hashed password string
        """
        ...

    @abstractmethod
    def verify(self, plain_password: str, hashed_password: str) -> bool:
        """
        Verify a plain text password against a hashed password.

        Args:
            plain_password: Plain text password to verify
            hashed_password: Previously hashed password

        Returns:
            True if passwords match, False otherwise
        """
        ...


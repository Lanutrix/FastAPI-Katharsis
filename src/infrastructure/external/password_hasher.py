"""Password hasher implementation."""

from passlib.context import CryptContext

from src.application.interfaces.password_hasher import IPasswordHasher


class PasswordHasher(IPasswordHasher):
    """Password hasher using bcrypt via passlib."""

    def __init__(self):
        self._context = CryptContext(schemes=["bcrypt"], deprecated="auto")

    def hash(self, password: str) -> str:
        """Hash a plain text password."""
        return self._context.hash(password)

    def verify(self, plain_password: str, hashed_password: str) -> bool:
        """Verify a plain text password against a hashed password."""
        return self._context.verify(plain_password, hashed_password)


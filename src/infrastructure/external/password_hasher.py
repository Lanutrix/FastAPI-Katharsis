"""Password hasher implementation."""

import bcrypt

from src.application.interfaces.password_hasher import IPasswordHasher


class PasswordHasher(IPasswordHasher):
    """Password hasher using bcrypt directly."""

    def hash(self, password: str) -> str:
        """Hash a plain text password."""
        return bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()

    def verify(self, plain_password: str, hashed_password: str) -> bool:
        """Verify a plain text password against a hashed password."""
        return bcrypt.checkpw(plain_password.encode(), hashed_password.encode())


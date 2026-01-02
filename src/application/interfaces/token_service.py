"""Token service interface."""

from abc import ABC, abstractmethod

from src.application.dto.token import TokenDTO, TokenPayloadDTO


class ITokenService(ABC):
    """Abstract interface for JWT token operations."""

    @abstractmethod
    def create_access_token(self, user_id: int) -> str:
        """
        Create an access token for a user.

        Args:
            user_id: The user's unique identifier

        Returns:
            Encoded JWT access token
        """
        ...

    @abstractmethod
    def create_refresh_token(self, user_id: int) -> str:
        """
        Create a refresh token for a user.

        Args:
            user_id: The user's unique identifier

        Returns:
            Encoded JWT refresh token
        """
        ...

    @abstractmethod
    def create_token_pair(self, user_id: int) -> TokenDTO:
        """
        Create both access and refresh tokens for a user.

        Args:
            user_id: The user's unique identifier

        Returns:
            TokenDTO containing both tokens
        """
        ...

    @abstractmethod
    def decode_token(self, token: str) -> TokenPayloadDTO:
        """
        Decode and validate a JWT token.

        Args:
            token: The encoded JWT token

        Returns:
            TokenPayloadDTO with decoded payload

        Raises:
            InvalidTokenError: If token is invalid or expired
        """
        ...

    @abstractmethod
    def verify_access_token(self, token: str) -> TokenPayloadDTO:
        """
        Verify an access token.

        Args:
            token: The encoded JWT access token

        Returns:
            TokenPayloadDTO with decoded payload

        Raises:
            InvalidTokenError: If token is invalid, expired, or not an access token
        """
        ...

    @abstractmethod
    def verify_refresh_token(self, token: str) -> TokenPayloadDTO:
        """
        Verify a refresh token.

        Args:
            token: The encoded JWT refresh token

        Returns:
            TokenPayloadDTO with decoded payload

        Raises:
            InvalidTokenError: If token is invalid, expired, or not a refresh token
        """
        ...


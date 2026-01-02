"""JWT service implementation."""

from datetime import datetime, timedelta
from uuid import UUID

from jose import JWTError, jwt

from src.application.dto.token import TokenDTO, TokenPayloadDTO
from src.application.interfaces.token_service import ITokenService
from src.domain.exceptions import InvalidTokenError
from src.infrastructure.config import get_settings


class JWTService(ITokenService):
    """JWT token service implementation using python-jose."""

    def __init__(self):
        settings = get_settings()
        self._secret_key = settings.jwt_secret_key
        self._algorithm = settings.jwt_algorithm
        self._access_token_expire_minutes = settings.jwt_access_token_expire_minutes
        self._refresh_token_expire_days = settings.jwt_refresh_token_expire_days

    def _create_token(self, user_id: UUID, token_type: str, expires_delta: timedelta) -> str:
        """Create a JWT token with given parameters."""
        expire = datetime.utcnow() + expires_delta
        payload = {
            "sub": str(user_id),
            "exp": expire,
            "type": token_type,
            "iat": datetime.utcnow(),
        }
        return jwt.encode(payload, self._secret_key, algorithm=self._algorithm)

    def create_access_token(self, user_id: UUID) -> str:
        """Create an access token for a user."""
        expires_delta = timedelta(minutes=self._access_token_expire_minutes)
        return self._create_token(user_id, "access", expires_delta)

    def create_refresh_token(self, user_id: UUID) -> str:
        """Create a refresh token for a user."""
        expires_delta = timedelta(days=self._refresh_token_expire_days)
        return self._create_token(user_id, "refresh", expires_delta)

    def create_token_pair(self, user_id: UUID) -> TokenDTO:
        """Create both access and refresh tokens for a user."""
        return TokenDTO(
            access_token=self.create_access_token(user_id),
            refresh_token=self.create_refresh_token(user_id),
        )

    def decode_token(self, token: str) -> TokenPayloadDTO:
        """Decode and validate a JWT token."""
        try:
            payload = jwt.decode(token, self._secret_key, algorithms=[self._algorithm])
            return TokenPayloadDTO(
                sub=UUID(payload["sub"]),
                exp=payload["exp"],
                type=payload["type"],
            )
        except JWTError as e:
            raise InvalidTokenError(f"Invalid token: {e}")
        except (KeyError, ValueError) as e:
            raise InvalidTokenError(f"Malformed token payload: {e}")

    def verify_access_token(self, token: str) -> TokenPayloadDTO:
        """Verify an access token."""
        payload = self.decode_token(token)
        if payload.type != "access":
            raise InvalidTokenError("Token is not an access token")
        return payload

    def verify_refresh_token(self, token: str) -> TokenPayloadDTO:
        """Verify a refresh token."""
        payload = self.decode_token(token)
        if payload.type != "refresh":
            raise InvalidTokenError("Token is not a refresh token")
        return payload


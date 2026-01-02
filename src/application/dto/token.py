"""Token-related Data Transfer Objects."""

from dataclasses import dataclass
from uuid import UUID


@dataclass(frozen=True)
class TokenDTO:
    """DTO for JWT token response."""

    access_token: str
    refresh_token: str
    token_type: str = "bearer"


@dataclass(frozen=True)
class TokenPayloadDTO:
    """DTO for decoded token payload."""

    sub: UUID  # user id
    exp: int  # expiration timestamp
    type: str  # "access" or "refresh"


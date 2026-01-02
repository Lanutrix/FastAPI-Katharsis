"""Token-related Data Transfer Objects."""

from dataclasses import dataclass


@dataclass(frozen=True)
class TokenDTO:
    """DTO for JWT token response."""

    access_token: str
    refresh_token: str


@dataclass(frozen=True)
class TokenPayloadDTO:
    """DTO for decoded token payload."""

    sub: int  # user id
    exp: int  # expiration timestamp
    type: str  # "access" or "refresh"


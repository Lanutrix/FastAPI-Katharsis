"""User-related Data Transfer Objects."""

from dataclasses import dataclass
from datetime import datetime


@dataclass(frozen=True)
class UserCreateDTO:
    """DTO for creating a new user."""

    email: str
    username: str
    password: str


@dataclass(frozen=True)
class UserResponseDTO:
    """DTO for user response data."""

    id: int
    email: str
    username: str
    created_at: datetime


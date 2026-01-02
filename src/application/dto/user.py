"""User-related Data Transfer Objects."""

from dataclasses import dataclass
from datetime import datetime
from uuid import UUID


@dataclass(frozen=True)
class UserCreateDTO:
    """DTO for creating a new user."""

    email: str
    username: str
    password: str


@dataclass(frozen=True)
class UserResponseDTO:
    """DTO for user response data."""

    id: UUID
    email: str
    username: str
    is_active: bool
    created_at: datetime


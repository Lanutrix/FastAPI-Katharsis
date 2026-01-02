from dataclasses import dataclass, field
from datetime import datetime


@dataclass
class User:
    """Domain entity representing a user in the system."""

    email: str
    username: str
    hashed_password: str
    id: int | None = None
    created_at: datetime = field(default_factory=datetime.utcnow)
    updated_at: datetime | None = None


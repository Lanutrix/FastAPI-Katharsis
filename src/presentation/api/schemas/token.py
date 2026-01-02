"""Token-related Pydantic schemas."""

from pydantic import BaseModel


class Token(BaseModel):
    """Schema for token response."""

    access_token: str
    refresh_token: str


class TokenRefresh(BaseModel):
    """Schema for token refresh request."""

    refresh_token: str


"""Math-related Pydantic schemas."""

from pydantic import BaseModel


class PrimesListRequest(BaseModel):
    """Schema for primes list request."""

    limit: int


class PrimesListResponse(BaseModel):
    """Schema for primes list response."""

    limit: int
    primes: list[int]
    count: int

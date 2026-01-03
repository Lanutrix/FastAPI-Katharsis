"""Math-related Data Transfer Objects."""

from dataclasses import dataclass


@dataclass(frozen=True)
class PrimesListRequestDTO:
    """DTO for primes list request."""

    limit: int


@dataclass(frozen=True)
class PrimesListResponseDTO:
    """DTO for primes list response."""

    limit: int
    primes: list[int]
    count: int

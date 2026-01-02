"""Math-related Data Transfer Objects."""

from dataclasses import dataclass


@dataclass(frozen=True)
class FactorialRequestDTO:
    """DTO for factorial calculation request."""

    number: int


@dataclass(frozen=True)
class FactorialResponseDTO:
    """DTO for factorial calculation response."""

    number: int
    result: int


@dataclass(frozen=True)
class PrimeCheckRequestDTO:
    """DTO for prime check request."""

    number: int


@dataclass(frozen=True)
class PrimeCheckResponseDTO:
    """DTO for prime check response."""

    number: int
    is_prime: bool


@dataclass(frozen=True)
class PowerRequestDTO:
    """DTO for power calculation request."""

    base: float
    exponent: float


@dataclass(frozen=True)
class PowerResponseDTO:
    """DTO for power calculation response."""

    base: float
    exponent: float
    result: float


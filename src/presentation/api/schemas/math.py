"""Math-related Pydantic schemas."""

from pydantic import BaseModel


class FactorialRequest(BaseModel):
    """Schema for factorial calculation request."""

    number: int


class FactorialResponse(BaseModel):
    """Schema for factorial calculation response."""

    number: int
    result: int


class PrimeCheckRequest(BaseModel):
    """Schema for prime check request."""

    number: int


class PrimeCheckResponse(BaseModel):
    """Schema for prime check response."""

    number: int
    is_prime: bool


class PowerRequest(BaseModel):
    """Schema for power calculation request."""

    base: float
    exponent: float


class PowerResponse(BaseModel):
    """Schema for power calculation response."""

    base: float
    exponent: float
    result: float


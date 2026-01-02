"""Math operations use case."""

from src.application.dto.math import (
    FactorialRequestDTO,
    FactorialResponseDTO,
    PowerRequestDTO,
    PowerResponseDTO,
    PrimeCheckRequestDTO,
    PrimeCheckResponseDTO,
)
from src.domain.exceptions import MathOperationError
from src.domain.models.math_operations import factorial, is_prime, power


class MathUseCase:
    """Use case for mathematical operations."""

    def calculate_factorial(self, dto: FactorialRequestDTO) -> FactorialResponseDTO:
        """
        Calculate factorial of a number.

        Args:
            dto: Factorial request with number

        Returns:
            Factorial response with result

        Raises:
            MathOperationError: If calculation fails
        """
        try:
            result = factorial(dto.number)
            return FactorialResponseDTO(number=dto.number, result=result)
        except ValueError as e:
            raise MathOperationError(str(e))

    def check_prime(self, dto: PrimeCheckRequestDTO) -> PrimeCheckResponseDTO:
        """
        Check if a number is prime.

        Args:
            dto: Prime check request with number

        Returns:
            Prime check response with result
        """
        result = is_prime(dto.number)
        return PrimeCheckResponseDTO(number=dto.number, is_prime=result)

    def calculate_power(self, dto: PowerRequestDTO) -> PowerResponseDTO:
        """
        Calculate power of a number.

        Args:
            dto: Power request with base and exponent

        Returns:
            Power response with result

        Raises:
            MathOperationError: If calculation fails
        """
        try:
            result = power(dto.base, dto.exponent)
            return PowerResponseDTO(base=dto.base, exponent=dto.exponent, result=result)
        except (ValueError, OverflowError) as e:
            raise MathOperationError(str(e))


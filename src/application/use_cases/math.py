"""Math operations use case."""

from src.application.dto.math import (
    PrimesListRequestDTO,
    PrimesListResponseDTO,
)
from src.domain.exceptions import MathOperationError
from src.domain.models.math_operations import primes_up_to


class MathUseCase:
    """Use case for mathematical operations."""

    def get_primes_list(self, dto: PrimesListRequestDTO) -> PrimesListResponseDTO:
        """
        Get all prime numbers up to a given limit.

        Args:
            dto: Primes list request with limit

        Returns:
            Primes list response with all primes up to limit

        Raises:
            MathOperationError: If calculation fails
        """
        try:
            primes = primes_up_to(dto.limit)
            return PrimesListResponseDTO(limit=dto.limit, primes=primes, count=len(primes))
        except ValueError as e:
            raise MathOperationError(str(e))

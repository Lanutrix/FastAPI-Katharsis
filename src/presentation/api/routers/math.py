"""Math operations router."""

from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status

from src.application.dto.math import (
    FactorialRequestDTO,
    PowerRequestDTO,
    PrimeCheckRequestDTO,
)
from src.application.dto.user import UserResponseDTO
from src.application.use_cases.math import MathUseCase
from src.domain.exceptions import MathOperationError
from src.presentation.api.dependencies.auth import get_current_user
from src.presentation.api.schemas.math import (
    FactorialRequest,
    FactorialResponse,
    PowerRequest,
    PowerResponse,
    PrimeCheckRequest,
    PrimeCheckResponse,
)

router = APIRouter(prefix="/math", tags=["Math Operations"])


@router.post(
    "/factorial",
    response_model=FactorialResponse,
    summary="Calculate factorial",
)
async def calculate_factorial(
    request: FactorialRequest,
    _current_user: Annotated[UserResponseDTO, Depends(get_current_user)],
) -> FactorialResponse:
    """
    Calculate the factorial of a non-negative integer.

    **Requires authentication.**

    - **number**: Non-negative integer to calculate factorial for

    Returns n! (n factorial)
    """
    use_case = MathUseCase()

    try:
        result = use_case.calculate_factorial(FactorialRequestDTO(number=request.number))
    except MathOperationError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e),
        )

    return FactorialResponse(number=result.number, result=result.result)


@router.post(
    "/prime",
    response_model=PrimeCheckResponse,
    summary="Check if number is prime",
)
async def check_prime(
    request: PrimeCheckRequest,
    _current_user: Annotated[UserResponseDTO, Depends(get_current_user)],
) -> PrimeCheckResponse:
    """
    Check if a number is prime.

    **Requires authentication.**

    - **number**: Integer to check for primality

    Returns whether the number is prime.
    """
    use_case = MathUseCase()
    result = use_case.check_prime(PrimeCheckRequestDTO(number=request.number))

    return PrimeCheckResponse(number=result.number, is_prime=result.is_prime)


@router.post(
    "/power",
    response_model=PowerResponse,
    summary="Calculate power",
)
async def calculate_power(
    request: PowerRequest,
    _current_user: Annotated[UserResponseDTO, Depends(get_current_user)],
) -> PowerResponse:
    """
    Calculate base raised to the power of exponent.

    **Requires authentication.**

    - **base**: The base number
    - **exponent**: The exponent

    Returns base^exponent.
    """
    use_case = MathUseCase()

    try:
        result = use_case.calculate_power(
            PowerRequestDTO(base=request.base, exponent=request.exponent)
        )
    except MathOperationError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e),
        )

    return PowerResponse(base=result.base, exponent=result.exponent, result=result.result)


"""Math operations router."""

from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status

from src.application.dto.math import PrimesListRequestDTO
from src.application.dto.user import UserResponseDTO
from src.application.use_cases.math import MathUseCase
from src.domain.exceptions import MathOperationError
from src.presentation.api.dependencies.auth import get_current_user
from src.presentation.api.schemas.math import PrimesListRequest, PrimesListResponse

router = APIRouter(prefix="/math", tags=["Math Operations"])


@router.post(
    "/primes-list",
    response_model=PrimesListResponse,
    summary="Get all primes up to a limit",
)
async def get_primes_list(
    request: PrimesListRequest,
    _current_user: Annotated[UserResponseDTO, Depends(get_current_user)],
) -> PrimesListResponse:
    """
    Get all prime numbers from 1 to a given limit.

    **Requires authentication.**

    - **limit**: Upper limit (inclusive) to find primes up to

    Returns a list of all prime numbers up to the limit.
    """
    use_case = MathUseCase()

    try:
        result = use_case.get_primes_list(PrimesListRequestDTO(limit=request.limit))
    except MathOperationError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e),
        )

    return PrimesListResponse(limit=result.limit, primes=result.primes, count=result.count)

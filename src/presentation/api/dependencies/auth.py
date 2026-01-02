"""Authentication dependencies."""

from typing import Annotated

from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from sqlalchemy.ext.asyncio import AsyncSession

from src.application.dto.user import UserResponseDTO
from src.application.use_cases.auth import GetCurrentUserUseCase
from src.domain.exceptions import InvalidTokenError, UserNotFoundError
from src.infrastructure.db.repositories.user import UserRepository
from src.infrastructure.db.session import get_async_session
from src.infrastructure.external.jwt_service import JWTService

security = HTTPBearer()


async def get_current_user(
    credentials: Annotated[HTTPAuthorizationCredentials, Depends(security)],
    session: Annotated[AsyncSession, Depends(get_async_session)],
) -> UserResponseDTO:
    """
    Dependency to get the current authenticated user from JWT token.

    Args:
        credentials: HTTP Bearer token credentials
        session: Database session

    Returns:
        Current user data

    Raises:
        HTTPException: If token is invalid or user not found
    """
    token = credentials.credentials
    jwt_service = JWTService()

    try:
        payload = jwt_service.verify_access_token(token)
    except InvalidTokenError as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=str(e),
            headers={"WWW-Authenticate": "Bearer"},
        )

    user_repository = UserRepository(session)
    use_case = GetCurrentUserUseCase(user_repository)

    try:
        return await use_case.execute(payload.sub)
    except UserNotFoundError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not found",
            headers={"WWW-Authenticate": "Bearer"},
        )



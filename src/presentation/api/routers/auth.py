"""Authentication router."""

from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from src.application.dto.user import UserCreateDTO, UserResponseDTO
from src.application.use_cases.auth import (
    LoginUserUseCase,
    RefreshTokenUseCase,
    RegisterUserUseCase,
)
from src.domain.exceptions import (
    InactiveUserError,
    InvalidCredentialsError,
    InvalidTokenError,
    UserAlreadyExistsError,
    UserNotFoundError,
)
from src.infrastructure.db.repositories.user import UserRepository
from src.infrastructure.db.session import get_async_session
from src.infrastructure.external.jwt_service import JWTService
from src.infrastructure.external.password_hasher import PasswordHasher
from src.presentation.api.dependencies.auth import get_current_active_user
from src.presentation.api.schemas.token import Token, TokenRefresh
from src.presentation.api.schemas.user import UserAuth, UserCreate, UserResponse

router = APIRouter(prefix="/auth", tags=["Authentication"])


@router.post(
    "/register",
    response_model=UserResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Register a new user",
)
async def register(
    user_data: UserCreate,
    session: Annotated[AsyncSession, Depends(get_async_session)],
) -> UserResponse:
    """
    Register a new user account.

    - **email**: Valid email address (must be unique)
    - **username**: Username (3-50 characters, must be unique)
    - **password**: Password (8-100 characters)
    """
    user_repository = UserRepository(session)
    password_hasher = PasswordHasher()

    use_case = RegisterUserUseCase(user_repository, password_hasher)

    dto = UserCreateDTO(
        email=user_data.email,
        username=user_data.username,
        password=user_data.password,
    )

    try:
        result = await use_case.execute(dto)
    except UserAlreadyExistsError as e:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=str(e),
        )

    return UserResponse(
        id=result.id,
        email=result.email,
        username=result.username,
        is_active=result.is_active,
        created_at=result.created_at,
    )


@router.post(
    "/login",
    response_model=Token,
    summary="Login and get tokens",
)
async def login(
    credentials: UserAuth,
    session: Annotated[AsyncSession, Depends(get_async_session)],
) -> Token:
    """
    Authenticate user and return access and refresh tokens.

    - **email**: User's email address
    - **password**: User's password
    """
    user_repository = UserRepository(session)
    password_hasher = PasswordHasher()
    jwt_service = JWTService()

    use_case = LoginUserUseCase(user_repository, password_hasher, jwt_service)

    try:
        result = await use_case.execute(credentials.email, credentials.password)
    except InvalidCredentialsError as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=str(e),
            headers={"WWW-Authenticate": "Bearer"},
        )
    except InactiveUserError as e:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=str(e),
        )

    return Token(
        access_token=result.access_token,
        refresh_token=result.refresh_token,
        token_type=result.token_type,
    )


@router.post(
    "/refresh",
    response_model=Token,
    summary="Refresh access token",
)
async def refresh_token(
    token_data: TokenRefresh,
    session: Annotated[AsyncSession, Depends(get_async_session)],
) -> Token:
    """
    Get new access and refresh tokens using a valid refresh token.

    - **refresh_token**: Valid refresh token
    """
    user_repository = UserRepository(session)
    jwt_service = JWTService()

    use_case = RefreshTokenUseCase(user_repository, jwt_service)

    try:
        result = await use_case.execute(token_data.refresh_token)
    except InvalidTokenError as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=str(e),
            headers={"WWW-Authenticate": "Bearer"},
        )
    except UserNotFoundError as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=str(e),
            headers={"WWW-Authenticate": "Bearer"},
        )
    except InactiveUserError as e:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=str(e),
        )

    return Token(
        access_token=result.access_token,
        refresh_token=result.refresh_token,
        token_type=result.token_type,
    )


@router.get(
    "/me",
    response_model=UserResponse,
    summary="Get current user",
)
async def get_me(
    current_user: Annotated[UserResponseDTO, Depends(get_current_active_user)],
) -> UserResponse:
    """
    Get the currently authenticated user's information.

    Requires a valid access token in the Authorization header.
    """
    return UserResponse(
        id=current_user.id,
        email=current_user.email,
        username=current_user.username,
        is_active=current_user.is_active,
        created_at=current_user.created_at,
    )


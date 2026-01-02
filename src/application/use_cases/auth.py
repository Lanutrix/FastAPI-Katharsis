"""Authentication use cases."""

from src.application.dto.token import TokenDTO
from src.application.dto.user import UserCreateDTO, UserResponseDTO
from src.application.interfaces.password_hasher import IPasswordHasher
from src.application.interfaces.token_service import ITokenService
from src.application.interfaces.user_repository import IUserRepository
from src.domain.exceptions import (
    InvalidCredentialsError,
    UserAlreadyExistsError,
    UserNotFoundError,
)
from src.domain.models.user import User


class RegisterUserUseCase:
    """Use case for user registration."""

    def __init__(
        self,
        user_repository: IUserRepository,
        password_hasher: IPasswordHasher,
        token_service: ITokenService,
    ):
        self._user_repository = user_repository
        self._password_hasher = password_hasher
        self._token_service = token_service

    async def execute(self, dto: UserCreateDTO) -> TokenDTO:
        """
        Register a new user and return tokens.

        Args:
            dto: User creation data

        Returns:
            Token pair (access + refresh)

        Raises:
            UserAlreadyExistsError: If email already exists
        """
        existing_user = await self._user_repository.get_by_email(dto.email)
        if existing_user:
            raise UserAlreadyExistsError(dto.email)

        existing_username = await self._user_repository.get_by_username(dto.username)
        if existing_username:
            raise UserAlreadyExistsError(dto.username)

        hashed_password = self._password_hasher.hash(dto.password)

        user = User(
            email=dto.email,
            username=dto.username,
            hashed_password=hashed_password,
        )

        created_user = await self._user_repository.create(user)

        return self._token_service.create_token_pair(created_user.id)


class LoginUserUseCase:
    """Use case for user login."""

    def __init__(
        self,
        user_repository: IUserRepository,
        password_hasher: IPasswordHasher,
        token_service: ITokenService,
    ):
        self._user_repository = user_repository
        self._password_hasher = password_hasher
        self._token_service = token_service

    async def execute(self, email: str, password: str) -> TokenDTO:
        """
        Authenticate user and return tokens.

        Args:
            email: User's email
            password: User's password

        Returns:
            Token pair (access + refresh)

        Raises:
            InvalidCredentialsError: If credentials are invalid
        """
        user = await self._user_repository.get_by_email(email)
        if not user:
            raise InvalidCredentialsError()

        if not self._password_hasher.verify(password, user.hashed_password):
            raise InvalidCredentialsError()

        return self._token_service.create_token_pair(user.id)


class RefreshTokenUseCase:
    """Use case for refreshing access token."""

    def __init__(
        self,
        user_repository: IUserRepository,
        token_service: ITokenService,
    ):
        self._user_repository = user_repository
        self._token_service = token_service

    async def execute(self, refresh_token: str) -> TokenDTO:
        """
        Refresh access token using a valid refresh token.

        Args:
            refresh_token: Valid refresh token

        Returns:
            New token pair

        Raises:
            InvalidTokenError: If refresh token is invalid
            UserNotFoundError: If user no longer exists
        """
        payload = self._token_service.verify_refresh_token(refresh_token)

        user = await self._user_repository.get_by_id(payload.sub)
        if not user:
            raise UserNotFoundError(str(payload.sub))

        return self._token_service.create_token_pair(user.id)


class GetCurrentUserUseCase:
    """Use case for getting current authenticated user."""

    def __init__(self, user_repository: IUserRepository):
        self._user_repository = user_repository

    async def execute(self, user_id: int) -> UserResponseDTO:
        """
        Get user by ID.

        Args:
            user_id: User's unique identifier

        Returns:
            User response data

        Raises:
            UserNotFoundError: If user not found
        """
        user = await self._user_repository.get_by_id(user_id)
        if not user:
            raise UserNotFoundError(str(user_id))

        return UserResponseDTO(
            id=user.id,
            email=user.email,
            username=user.username,
            created_at=user.created_at,
        )


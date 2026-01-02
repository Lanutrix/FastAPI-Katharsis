"""User repository interface."""

from abc import ABC, abstractmethod

from src.domain.models.user import User


class IUserRepository(ABC):
    """Abstract interface for user data persistence."""

    @abstractmethod
    async def create(self, user: User) -> User:
        """
        Persist a new user.

        Args:
            user: User domain entity to persist

        Returns:
            The persisted user with updated fields
        """
        ...

    @abstractmethod
    async def get_by_id(self, user_id: int) -> User | None:
        """
        Retrieve a user by their ID.

        Args:
            user_id: The user's unique identifier

        Returns:
            User if found, None otherwise
        """
        ...

    @abstractmethod
    async def get_by_email(self, email: str) -> User | None:
        """
        Retrieve a user by their email.

        Args:
            email: The user's email address

        Returns:
            User if found, None otherwise
        """
        ...

    @abstractmethod
    async def get_by_username(self, username: str) -> User | None:
        """
        Retrieve a user by their username.

        Args:
            username: The user's username

        Returns:
            User if found, None otherwise
        """
        ...

    @abstractmethod
    async def update(self, user: User) -> User:
        """
        Update an existing user.

        Args:
            user: User domain entity with updated fields

        Returns:
            The updated user
        """
        ...

    @abstractmethod
    async def delete(self, user_id: int) -> bool:
        """
        Delete a user by their ID.

        Args:
            user_id: The user's unique identifier

        Returns:
            True if deleted, False if not found
        """
        ...


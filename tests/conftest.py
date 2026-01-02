"""Shared test fixtures with in-memory SQLite database."""

from collections.abc import AsyncGenerator

import pytest
from httpx import ASGITransport, AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from sqlalchemy.pool import StaticPool

from src.infrastructure.db.models.base import Base
from src.infrastructure.db.session import get_async_session
from src.presentation.main import app

# In-memory SQLite for fast tests
_test_engine = create_async_engine(
    "sqlite+aiosqlite:///:memory:",
    echo=False,
    poolclass=StaticPool,
    connect_args={"check_same_thread": False},
)

_TestAsyncSessionLocal = async_sessionmaker(
    _test_engine,
    class_=AsyncSession,
    expire_on_commit=False,
    autocommit=False,
    autoflush=False,
)


@pytest.fixture(scope="session")
async def setup_database():
    """Create tables once per test session."""
    async with _test_engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield
    await _test_engine.dispose()


@pytest.fixture(scope="function")
async def test_session(setup_database) -> AsyncGenerator[AsyncSession, None]:
    """Provide a test database session with cleanup."""
    async with _TestAsyncSessionLocal() as session:
        yield session
        # Clean up data after test
        for table in reversed(Base.metadata.sorted_tables):
            await session.execute(table.delete())
        await session.commit()


@pytest.fixture(scope="function")
async def client(setup_database) -> AsyncGenerator[AsyncClient, None]:
    """Provide an async HTTP client for testing."""

    async def override_get_async_session() -> AsyncGenerator[AsyncSession, None]:
        async with _TestAsyncSessionLocal() as session:
            try:
                yield session
                await session.commit()
            except Exception:
                await session.rollback()
                raise

    app.dependency_overrides[get_async_session] = override_get_async_session

    async with AsyncClient(
        transport=ASGITransport(app=app),
        base_url="http://test",
    ) as ac:
        yield ac

    app.dependency_overrides.clear()

    # Clean up data after test
    async with _TestAsyncSessionLocal() as session:
        for table in reversed(Base.metadata.sorted_tables):
            await session.execute(table.delete())
        await session.commit()


@pytest.fixture
async def registered_user(client: AsyncClient) -> dict:
    """Register a test user and return user data with tokens."""
    user_data = {
        "email": "test@example.com",
        "username": "testuser",
        "password": "testpassword123",
    }
    response = await client.post("/api/v1/auth/register", json=user_data)
    assert response.status_code == 201
    tokens = response.json()
    return {
        **user_data,
        "access_token": tokens["access_token"],
        "refresh_token": tokens["refresh_token"],
    }


@pytest.fixture
async def auth_headers(registered_user: dict) -> dict:
    """Provide authorization headers with valid access token."""
    return {"Authorization": f"Bearer {registered_user['access_token']}"}

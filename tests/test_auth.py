"""Tests for authentication endpoints."""

import pytest
from httpx import AsyncClient


@pytest.mark.asyncio
async def test_register_success(client: AsyncClient) -> None:
    """Test successful user registration."""
    user_data = {
        "email": "newuser@example.com",
        "username": "newuser",
        "password": "securepassword123",
    }
    response = await client.post("/api/v1/auth/register", json=user_data)

    assert response.status_code == 201
    data = response.json()
    assert "access_token" in data
    assert "refresh_token" in data


@pytest.mark.asyncio
async def test_register_duplicate_email(client: AsyncClient) -> None:
    """Test registration with duplicate email fails."""
    user_data = {
        "email": "duplicate@example.com",
        "username": "user1",
        "password": "securepassword123",
    }
    # First registration
    response = await client.post("/api/v1/auth/register", json=user_data)
    assert response.status_code == 201

    # Second registration with same email
    user_data["username"] = "user2"
    response = await client.post("/api/v1/auth/register", json=user_data)

    assert response.status_code == 409


@pytest.mark.asyncio
async def test_login_success(client: AsyncClient, registered_user: dict) -> None:
    """Test successful login."""
    login_data = {
        "email": registered_user["email"],
        "password": registered_user["password"],
    }
    response = await client.post("/api/v1/auth/login", json=login_data)

    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data
    assert "refresh_token" in data


@pytest.mark.asyncio
async def test_login_invalid_credentials(client: AsyncClient) -> None:
    """Test login with invalid credentials fails."""
    login_data = {
        "email": "nonexistent@example.com",
        "password": "wrongpassword",
    }
    response = await client.post("/api/v1/auth/login", json=login_data)

    assert response.status_code == 401


@pytest.mark.asyncio
async def test_refresh_token(client: AsyncClient, registered_user: dict) -> None:
    """Test token refresh."""
    refresh_data = {
        "refresh_token": registered_user["refresh_token"],
    }
    response = await client.post("/api/v1/auth/refresh", json=refresh_data)

    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data
    assert "refresh_token" in data


@pytest.mark.asyncio
async def test_get_me(client: AsyncClient, registered_user: dict, auth_headers: dict) -> None:
    """Test get current user endpoint."""
    response = await client.get("/api/v1/auth/me", headers=auth_headers)

    assert response.status_code == 200
    data = response.json()
    assert data["email"] == registered_user["email"]
    assert data["username"] == registered_user["username"]
    assert "id" in data
    assert "created_at" in data


@pytest.mark.asyncio
async def test_get_me_unauthorized(client: AsyncClient) -> None:
    """Test get current user without token fails."""
    response = await client.get("/api/v1/auth/me")

    assert response.status_code == 403


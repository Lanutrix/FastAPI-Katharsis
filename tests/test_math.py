"""Tests for math endpoints."""

import pytest
from httpx import AsyncClient


@pytest.mark.asyncio
async def test_primes_list_success(client: AsyncClient, auth_headers: dict) -> None:
    """Test primes list with valid input."""
    response = await client.post(
        "/api/v1/math/primes-list",
        json={"limit": 20},
        headers=auth_headers,
    )

    assert response.status_code == 200
    data = response.json()
    assert data["limit"] == 20
    assert data["primes"] == [2, 3, 5, 7, 11, 13, 17, 19]
    assert data["count"] == 8


@pytest.mark.asyncio
async def test_primes_list_small_limit(client: AsyncClient, auth_headers: dict) -> None:
    """Test primes list with limit below 2 returns empty."""
    response = await client.post(
        "/api/v1/math/primes-list",
        json={"limit": 1},
        headers=auth_headers,
    )

    assert response.status_code == 200
    data = response.json()
    assert data["limit"] == 1
    assert data["primes"] == []
    assert data["count"] == 0


@pytest.mark.asyncio
async def test_primes_list_invalid_limit(client: AsyncClient, auth_headers: dict) -> None:
    """Test primes list with limit less than 1 fails."""
    response = await client.post(
        "/api/v1/math/primes-list",
        json={"limit": 0},
        headers=auth_headers,
    )

    assert response.status_code == 400


@pytest.mark.asyncio
async def test_primes_list_unauthorized(client: AsyncClient) -> None:
    """Test primes list endpoint without authentication fails."""
    response = await client.post(
        "/api/v1/math/primes-list",
        json={"limit": 10},
    )

    assert response.status_code == 403

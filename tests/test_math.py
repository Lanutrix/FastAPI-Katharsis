"""Tests for math endpoints."""

import pytest
from httpx import AsyncClient


@pytest.mark.asyncio
async def test_factorial_success(client: AsyncClient, auth_headers: dict) -> None:
    """Test factorial calculation with valid input."""
    response = await client.post(
        "/api/v1/math/factorial",
        json={"number": 5},
        headers=auth_headers,
    )

    assert response.status_code == 200
    data = response.json()
    assert data["number"] == 5
    assert data["result"] == 120


@pytest.mark.asyncio
async def test_factorial_zero(client: AsyncClient, auth_headers: dict) -> None:
    """Test factorial of zero."""
    response = await client.post(
        "/api/v1/math/factorial",
        json={"number": 0},
        headers=auth_headers,
    )

    assert response.status_code == 200
    data = response.json()
    assert data["number"] == 0
    assert data["result"] == 1


@pytest.mark.asyncio
async def test_factorial_negative(client: AsyncClient, auth_headers: dict) -> None:
    """Test factorial with negative number fails."""
    response = await client.post(
        "/api/v1/math/factorial",
        json={"number": -5},
        headers=auth_headers,
    )

    assert response.status_code == 400


@pytest.mark.asyncio
async def test_prime_check_true(client: AsyncClient, auth_headers: dict) -> None:
    """Test prime check with a prime number."""
    response = await client.post(
        "/api/v1/math/prime",
        json={"number": 17},
        headers=auth_headers,
    )

    assert response.status_code == 200
    data = response.json()
    assert data["number"] == 17
    assert data["is_prime"] is True


@pytest.mark.asyncio
async def test_prime_check_false(client: AsyncClient, auth_headers: dict) -> None:
    """Test prime check with a non-prime number."""
    response = await client.post(
        "/api/v1/math/prime",
        json={"number": 15},
        headers=auth_headers,
    )

    assert response.status_code == 200
    data = response.json()
    assert data["number"] == 15
    assert data["is_prime"] is False


@pytest.mark.asyncio
async def test_power_success(client: AsyncClient, auth_headers: dict) -> None:
    """Test power calculation."""
    response = await client.post(
        "/api/v1/math/power",
        json={"base": 2.0, "exponent": 10.0},
        headers=auth_headers,
    )

    assert response.status_code == 200
    data = response.json()
    assert data["base"] == 2.0
    assert data["exponent"] == 10.0
    assert data["result"] == 1024.0


@pytest.mark.asyncio
async def test_power_fractional_exponent(client: AsyncClient, auth_headers: dict) -> None:
    """Test power with fractional exponent (square root)."""
    response = await client.post(
        "/api/v1/math/power",
        json={"base": 9.0, "exponent": 0.5},
        headers=auth_headers,
    )

    assert response.status_code == 200
    data = response.json()
    assert data["result"] == 3.0


@pytest.mark.asyncio
async def test_math_factorial_unauthorized(client: AsyncClient) -> None:
    """Test factorial endpoint without authentication fails."""
    response = await client.post(
        "/api/v1/math/factorial",
        json={"number": 5},
    )

    assert response.status_code == 403


@pytest.mark.asyncio
async def test_math_prime_unauthorized(client: AsyncClient) -> None:
    """Test prime check endpoint without authentication fails."""
    response = await client.post(
        "/api/v1/math/prime",
        json={"number": 17},
    )

    assert response.status_code == 403


@pytest.mark.asyncio
async def test_math_power_unauthorized(client: AsyncClient) -> None:
    """Test power endpoint without authentication fails."""
    response = await client.post(
        "/api/v1/math/power",
        json={"base": 2.0, "exponent": 3.0},
    )

    assert response.status_code == 403


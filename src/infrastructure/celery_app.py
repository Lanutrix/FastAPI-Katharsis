"""Celery application configuration and tasks."""

from celery import Celery

from src.domain.models.math_operations import primes_up_to
from src.infrastructure.config import get_settings

settings = get_settings()

# Create Celery app
app = Celery(
    "katharsis",
    broker=settings.redis_url,
    backend=settings.redis_url,
)

# Celery configuration
app.conf.update(
    task_serializer="json",
    accept_content=["json"],
    result_serializer="json",
    timezone="UTC",
    enable_utc=True,
    task_track_started=True,
    result_expires=3600,  # Results expire after 1 hour
)


@app.task(name="primes_list")
def primes_list_task(limit: int) -> dict:
    """
    Celery task to compute all prime numbers up to a given limit.

    Args:
        limit: Upper limit (inclusive) to find primes up to

    Returns:
        Dictionary with limit, primes list, and count
    """
    primes = primes_up_to(limit)
    return {
        "limit": limit,
        "primes": primes,
        "count": len(primes),
    }


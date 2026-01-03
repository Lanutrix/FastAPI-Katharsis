"""Pure domain functions for mathematical operations."""


def primes_up_to(n: int) -> list[int]:
    """
    Get all prime numbers from 1 to n (inclusive).

    Uses the Sieve of Eratosthenes algorithm for efficiency.

    Args:
        n: Upper limit (inclusive)

    Returns:
        List of all prime numbers from 1 to n

    Raises:
        ValueError: If n is less than 1
    """
    if n < 1:
        raise ValueError("Input must be at least 1")
    if n < 2:
        return []

    sieve = [True] * (n + 1)
    sieve[0] = sieve[1] = False

    for i in range(2, int(n**0.5) + 1):
        if sieve[i]:
            for j in range(i * i, n + 1, i):
                sieve[j] = False

    return [i for i, is_prime in enumerate(sieve) if is_prime]

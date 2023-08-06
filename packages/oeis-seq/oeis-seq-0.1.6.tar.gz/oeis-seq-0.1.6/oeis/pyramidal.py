# coding=utf-8
from itertools import count
from typing import Iterable

from .registry import registry


def pyramidal(r: int) -> Iterable[int]:
    """
    Pyramidal numbers.

    Args:
            r: # of sides.
    """
    yield 0
    for n in count(start=1):
        yield (3 * pow(n, 2) + (pow(n, 3) * (r - 2)) - n * (r - 5)) // 6


@registry.register("A000292")
def triangular_pyramidal() -> Iterable[int]:
    """Triangular pyramidal numbers."""
    return pyramidal(3)


@registry.register("A000330")
def square_pyramidal() -> Iterable[int]:
    """Square pyramidal numbers."""
    return pyramidal(4)


@registry.register("A002411")
def pentagonal_pyramidal() -> Iterable[int]:
    """Pentagonal pyramidal numbers."""
    return pyramidal(5)


@registry.register("A002412")
def hexagonal_pyramidal() -> Iterable[int]:
    """Hexagonal pyramidal numbers."""
    return pyramidal(6)


@registry.register("A002413")
def heptagonal_pyramidal() -> Iterable[int]:
    """Heptagonal pyramidal numbers."""
    return pyramidal(7)


@registry.register("A002414")
def octagonal_pyramidal() -> Iterable[int]:
    """Octagonal pyramidal numbers."""
    return pyramidal(8)

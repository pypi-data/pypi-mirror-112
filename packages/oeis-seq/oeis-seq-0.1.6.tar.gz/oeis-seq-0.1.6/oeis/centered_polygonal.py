# coding=utf-8
from itertools import count
from typing import Iterable

from oeis.registry import registry


def centered_polygonal(k: int) -> Iterable[int]:
    """
    Centered polygonal numbers.

    Args:
            k: # of sides.
    """
    yield 1
    for n in count(start=1):
        yield ((k * n * (n + 1)) // 2) + 1


@registry.register("A005448")
def centered_triangular() -> Iterable[int]:
    """Centered triangular numbers."""
    return centered_polygonal(3)


@registry.register("A001844")
def centered_square() -> Iterable[int]:
    """Centered square numbers."""
    return centered_polygonal(4)


@registry.register("A005891")
def centered_pentagonal() -> Iterable[int]:
    """Centered pentagonal numbers."""
    return centered_polygonal(5)


@registry.register("A003215")
def centered_hexagonal() -> Iterable[int]:
    """Centered hexagonal numbers."""
    return centered_polygonal(6)


@registry.register("A069099")
def centered_heptagonal() -> Iterable[int]:
    """Centered heptagonal numbers."""
    return centered_polygonal(7)


@registry.register("A016754")
def centered_octagonal() -> Iterable[int]:
    """Centered octagonal numbers."""
    return centered_polygonal(8)


@registry.register("A060544")
def centered_nonagonal() -> Iterable[int]:
    """Centered nonagonal numbers."""
    return centered_polygonal(9)


@registry.register("A062786")
def centered_decagonal() -> Iterable[int]:
    """Centered decagonal numbers."""
    return centered_polygonal(10)


@registry.register("A069125")
def centered_hendecagonal() -> Iterable[int]:
    """Centered hendecagonal numbers."""
    return centered_polygonal(11)


@registry.register("A003154")
def centered_dodecagonal() -> Iterable[int]:
    """Centered dodecagonal numbers."""
    return centered_polygonal(12)

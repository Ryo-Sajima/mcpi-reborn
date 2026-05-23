"""Simple 3D vector utility used by the mcpi client.

This implements a minimal immutable-like vector with convenient numeric
operations. The implementation is intentionally small and depends only on
the Python standard library.

Examples
--------
>>> from mcpi.vec3 import Vec3
>>> a = Vec3(1, 2, 3)
>>> b = Vec3(0.5, 0, -1)
>>> a + b
Vec3(1.5, 2.0, 2.0)

Notes
-----
This class provides ``+`` and ``-`` operators; operations accept another
``Vec3`` or any iterable of three numeric values.
"""

from __future__ import annotations

from typing import Iterable, Tuple, Iterator, cast

# A numeric type accepted by Vec3 operations
Number = int | float


class Vec3[T: Number]:
    """3D vector.

    Parameters
    ----------
    x, y, z : int | float
        Coordinates of the vector. Values may be integers or floats; the
        precise numeric type is preserved when constructing a ``Vec3``.

    Notes
    -----
    Instances are mutable but arithmetic operations return new
    :class:`Vec3` objects.
    """

    def __init__(self, x: T = cast(T, 0), y: T = cast(T, 0), z: T = cast(T, 0)) -> None:
        self.x: T = x
        self.y: T = y
        self.z: T = z

    def __iter__(self) -> Iterator[T]:
        """Iterate over coordinates in ``(x, y, z)`` order.

        The yielded numeric type matches the type that was supplied to the
        constructor (int or float), so integer tile vectors can be unpacked
        directly into APIs that expect ints.
        """
        yield self.x
        yield self.y
        yield self.z

    def to_tuple(self) -> Tuple[T, T, T]:
        """Return a ``(x, y, z)`` tuple.

        Returns
        -------
        tuple
            A 3-tuple preserving the numeric types of the coordinates.
        """
        return (self.x, self.y, self.z)

    def __add__(self, other: Iterable[Number]) -> "Vec3[Number]":
        """Vector addition.

        Parameters
        ----------
        other : iterable
            Another :class:`Vec3` or an iterable of three numbers.
        """
        ox, oy, oz = tuple(other)

        return Vec3(
            self.x + ox,
            self.y + oy,
            self.z + oz
        )

    def __radd__(self, other: Iterable[Number]) -> "Vec3[Number]":
        return self.__add__(other)

    def __sub__(self, other: Iterable[Number]) -> "Vec3[Number]":
        """Vector subtraction."""
        ox, oy, oz = tuple(other)

        return Vec3(
            self.x - ox,
            self.y - oy,
            self.z - oz
        )

    def __rsub__(self, other: Iterable[Number]) -> "Vec3[Number]":
        ox, oy, oz = tuple(other)

        return Vec3(
            ox - self.x,
            oy - self.y,
            oz - self.z
        )

    def __repr__(self) -> str:
        return f"Vec3({self.x}, {self.y}, {self.z})"

"""Simple code to test mypy."""

from collections.abc import Iterable, Mapping
from typing import Protocol


def add(a: int, b: int) -> int:
    """Compute the sum between two numbers.

    Args:
        a: First number
        b: Second number

    Returns:
        Sum of the two numbers.
    """
    return a + b


def total(numbers: Iterable[int]) -> int:
    """Compute the sum of an iterable of numbers.

    Args:
        numbers: Iterable of numbers

    Returns:
        Sum of the numbers.
    """
    total = 0
    for number in numbers:
        total += number
    return total


class SupportsUpper[T](Protocol):
    """Protocol for types that support upper."""

    def upper(self) -> T:
        """Apply upper on self."""
        ...


def upper_keys[T, U](mapping: Mapping[SupportsUpper[T], U]) -> dict[T, U]:
    """Create a dictionary with uppercase keys from a given dictionary.

    Params:
        mapping: Input mapping

    Returns:
        Dictionary with the uppercase keys.
    """
    result = {}
    for key, value in mapping.items():
        result[key.upper()] = value
    return result


if __name__ == "__main__":
    print("add(1, 2) →", add(1, 2))
    print("total([1, 2, 3]) →", total([1, 2, 3]))
    print('upper_keys({"a": 1, "b": 2}) →', upper_keys({"a": 1, "b": 2}))

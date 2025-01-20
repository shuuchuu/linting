"""Simple code to test mypy."""

from typing import Any


def add(a, b):
    """Compute the sum between two numbers.

    Args:
        a: First number
        b: Second number

    Returns:
        Sum of the two numbers.
    """
    return a + b


def total(numbers):
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


def upper_keys(mapping):
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


class Interval:
    """Interval manipulation."""

    def __init__(self, lower_bound: float, upper_bound: float) -> None:
        """Initialize an interval."""
        self._lower_bound = lower_bound
        self._upper_bound = upper_bound

    def upper(self) -> float:
        """Get the upper bound of the interval.

        Returns:
            The upper bound of the interval.
        """
        return self._upper_bound

    def lower(self) -> float:
        """Get the lower bound of the interval.

        Returns:
            The lower bound of the interval.
        """
        return self._lower_bound

    def __contains__(self, item: Any) -> bool:
        """Test if item is in [lower_bound, upper_bound].

        Returns:
            True if item is in [lower_bound, upper_bound], False otherwise.
        """
        try:
            return self._lower_bound <= item <= self._upper_bound
        except TypeError:
            return False


if __name__ == "__main__":
    print("add(1, 2) →", add(1, 2))
    print("total([1, 2, 3]) →", total([1, 2, 3]))
    print('upper_keys({"a": 1, "b": 2}) →', upper_keys({"a": 1, "b": 2}))
    print(
        'upper_keys({Interval(1.0, 2.0): "abc"})',
        upper_keys({Interval(1.0, 2.0): "abc"}),
    )

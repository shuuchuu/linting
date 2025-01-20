"""Simple code to test mypy."""

from collections.abc import Iterable, Mapping


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


def upper_keys[T](mapping: Mapping[str, T]) -> dict[str, T]:
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
    print("Appel à add avec les arguments 1 et 2 :", add(1, 2))
    print("Appel à total avec l'argument [1, 2, 3] :", total([1, 2, 3]))
    print(
        'Appel à upper_keys avec l\'argument {"a": 1, "b": 2}',
        upper_keys({"a": 1, "b": 2}),
    )

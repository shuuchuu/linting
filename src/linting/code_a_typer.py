"""Code simple à typer."""

from collections.abc import Iterable, Mapping


def additionne(a: int, b: int) -> int:
    """Calcule la somme de deux nombres.

    Args:
        a: Premier nombre
        b: Deuxième nombre

    Returns:
        Somme des deux nombres.
    """
    return a + b


def totalise(nombres: Iterable[int]) -> int:
    """Calcule la somme d'un itérable de nombres.

    Args:
        nombres: Itérable de nombres

    Returns:
        Somme des nombres.
    """
    total = 0
    for nombre in nombres:
        total += nombre
    return total


def met_en_majuscules[T](dictionnaire: Mapping[str, T]) -> dict[str, T]:
    """Crée un dictionnaire aux clés en majuscules à partir d'un dictionnaire donné.

    Args:
        dictionnaire: Dictionnaire d'entrée

    Returns:
        Dictionnaire aux clés en majuscules.
    """
    resultat = {}
    for cle, valeur in dictionnaire.items():
        resultat[cle.upper()] = valeur
    return resultat


if __name__ == "__main__":
    print("additionne(1, 2) →", additionne(1, 2))  # noqa: T201
    print("totalise([1, 2, 3]) →", totalise([1, 2, 3]))  # noqa: T201
    print('met_en_majuscules({"a": 1, "b": 2}) →', met_en_majuscules({"a": 1, "b": 2}))  # noqa: T201

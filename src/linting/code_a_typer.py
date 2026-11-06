"""Code simple à typer."""


def additionne(a, b):
    """Calcule la somme de deux nombres.

    Args:
        a: Premier nombre
        b: Deuxième nombre

    Returns:
        Somme des deux nombres.
    """
    return a + b


def totalise(nombres):
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


def met_en_majuscules(dictionnaire):
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
    print("additionne(1, 2) →", additionne(1, 2))
    print("totalise([1, 2, 3]) →", totalise([1, 2, 3]))
    print('met_en_majuscules({"a": 1, "b": 2}) →', met_en_majuscules({"a": 1, "b": 2}))

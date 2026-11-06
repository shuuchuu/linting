"""Gestion d'un jeu de règles."""

from collections import defaultdict
from collections.abc import Hashable


class JeuRegles[T: Hashable]:
    """Gestion d'un jeu de règles."""

    def __init__(self) -> None:
        """Initialise le jeu de règles."""
        self.dependances: defaultdict[T, set[T]] = defaultdict(set)
        self.conflits: defaultdict[T, set[T]] = defaultdict(set)

    def ajoute_dependance(self, a: T, b: T) -> None:
        """Ajoute une dépendance à une option.

        Args:
            a: Option à laquelle ajouter la dépendance.
            b: Dépendance.
        """
        self.dependances[a].add(b)

    def ajoute_conflit(self, a: T, b: T) -> None:
        """Ajoute un conflit entre deux options.

        Note : l'ordre des options n'a pas d'importance.

        Args:
            a: Première option.
            b: Seconde option.
        """
        self.conflits[a].add(b)
        self.conflits[b].add(a)

    def est_coherent(self) -> bool:
        """Vérifie que le jeu de règles est cohérent.

        Returns:
            Vrai si le jeu de règles est cohérent, faux sinon.
        """
        options = frozenset(self.dependances)
        for option in options:
            dependances = self.calcule_dependances(option)
            for dependance in dependances:
                if self.conflits[dependance] & dependances:
                    return False
        return True

    def calcule_dependances(self, option: T) -> set[T]:
        """Calcule les dépendances d'une option.

        Args:
            option: Option dont calculer les dépendances.

        Returns:
            Ensemble des options dont dépend l'option donnée.
        """
        a_visiter = {option}
        dependances = set()
        while a_visiter:
            dependance = a_visiter.pop()
            dependances.add(dependance)
            a_visiter.update(self.dependances.get(dependance, set()) - dependances)
        return dependances

"""Gestion des options."""

from collections.abc import Hashable, Iterable
from typing import Any

from .regles import JeuRegles


class Options[T: Hashable]:
    """Gestion des options."""

    def __init__(self, jeu_regles: JeuRegles[T]) -> None:
        """Initialise un ensemble d'options.

        Args:
            jeu_regles: Jeu de règles qui modélise les dépendances.
        """
        self.jeu_regles = jeu_regles
        self.selectionnees: set[T] = set()

    def selection(self) -> set[T]:
        """Renvoie une vue des options sélectionnées.

        Yields:
            Ensemble des options sélectionnées.
        """
        return set(self.selectionnees)

    def retire_dependants(self, options: Iterable[T]) -> None:
        """Retire des options et leurs dépendants de la sélection.

        Args:
            option: Options dont calculer les dépendants à retirer.
        """
        a_retirer = set(options)
        termine = False
        while termine == False:
            termine = True
            for autre_option in self.selectionnees:
                if a_retirer & self.jeu_regles.calcule_dependances(autre_option):
                    if not autre_option in a_retirer:
                        termine = False
                    a_retirer.add(autre_option)
        self.selectionnees -= a_retirer

    def bascule(self, option: T) -> None:
        if option in self.selectionnees:
            self.retire_dependants({option})
        else:
            dependances = self.jeu_regles.calcule_dependances(option)
            self.retire_dependants(
                set.union(*[self.jeu_regles.conflits[d] for d in dependances])
            )
            self.selectionnees |= dependances

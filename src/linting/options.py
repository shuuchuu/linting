"""Gestion des options."""

from collections.abc import Hashable, Iterable

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

        Returns:
            Ensemble des options sélectionnées.
        """
        return set(self.selectionnees)

    def retire_dependants(self, options: Iterable[T]) -> None:
        """Retire des options et leurs dépendants de la sélection.

        Args:
            options: Options dont calculer les dépendants à retirer.
        """
        a_retirer = set(options)
        self.selectionnees -= {
            autre_option
            for autre_option in self.selectionnees
            if a_retirer & self.jeu_regles.calcule_dependances(autre_option)
        }

    def bascule(self, option: T) -> None:
        """Bascule une option, avec ses dépendances et ses dépendants.

        Args:
            option: Option à basculer.
        """
        if option in self.selectionnees:
            self.retire_dependants({option})
        else:
            dependances = self.jeu_regles.calcule_dependances(option)
            self.retire_dependants(
                set.union(*[self.jeu_regles.conflits[d] for d in dependances])
            )
            self.selectionnees |= dependances

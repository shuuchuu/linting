"""Options management."""

from collections.abc import Hashable, Iterable

from .ruleset import RuleSet


class Options[T: Hashable]:
    """Options management."""

    def __init__(self, rule_set: RuleSet[T]) -> None:
        """Initialize a set of options.

        Args:
            rule_set: RuleSet to use to model dependencies.
        """
        self.rule_set = rule_set
        self.selected: set[T] = set()

    def selection(self) -> set[T]:
        """Return a view of the selected options.

        Returns:
            Set of selected options.
        """
        return set(self.selected)

    def remove_dependents(self, options: Iterable[T]) -> None:
        """Remove options and their dependents from the selection.

        Args:
            options: Options to remove from the selection.
        """
        to_remove = set(options)
        done = False
        while not done:
            done = True
            for other_option in self.selected:
                if to_remove & self.rule_set.compute_deps(other_option):
                    if other_option not in to_remove:
                        done = False
                    to_remove.add(other_option)
        self.selected -= to_remove

    def toggle(self, option: T) -> None:
        """Toggle an option.

        Args:
            option: Which option to toggle.
        """
        if option in self.selected:
            self.remove_dependents({option})
        else:
            deps = self.rule_set.compute_deps(option)
            self.remove_dependents(
                set.union(*[self.rule_set.conflicts[d] for d in deps])
            )
            self.selected |= deps

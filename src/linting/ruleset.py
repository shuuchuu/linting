"""RuleSet management."""

from collections import defaultdict
from collections.abc import Hashable


class RuleSet[T: Hashable]:
    """RuleSet management."""

    def __init__(self) -> None:
        """Initialize the ruleset."""
        self.deps: defaultdict[T, set[T]] = defaultdict(set)
        self.conflicts: defaultdict[T, set[T]] = defaultdict(set)

    def add_dep(self, a: T, b: T) -> None:
        """Add a dependency to an option.

        Args:
            a: Option to add the dependency to.
            b: Dependency.
        """
        self.deps[a].add(b)

    def add_conflict(self, a: T, b: T) -> None:
        """Add a conflict between two options.

        Note: the order of options doesn't matter.

        Args:
            a: First option.
            b: Second option.
        """
        self.conflicts[a].add(b)
        self.conflicts[b].add(a)

    def is_coherent(self) -> bool:
        """Check that the ruleset is coherent.

        Returns:
            True if the ruleset is coherent, False otherwise.
        """
        options = frozenset(self.deps)
        for option in options:
            deps = self.compute_deps(option)
            for dep in deps:
                if self.conflicts[dep] & deps:
                    return False
        return True

    def compute_deps(self, option: T) -> set[T]:
        """Compute dependencies of an option.

        Params:
            option: Option to compute the dependencies of.

        Returns:
            The set of options on which the input option depends.
        """
        to_visit = {option}
        deps = set()
        while to_visit:
            dep = to_visit.pop()
            deps.add(dep)
            to_visit.update(self.deps.get(dep, set()) - deps)
        return deps

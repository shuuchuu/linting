"""Usage of bad_options.py and ruleset.py."""

from .options import Options
from .ruleset import RuleSet

if __name__ == "__main__":
    rs: RuleSet[str] = RuleSet()
    rs.add_dep("A", "B")
    rs.add_dep("B", "C")
    rs.add_dep("C", "D")

    options: Options[str] = Options(rs)
    options.toggle("A")
    print(options.selected)

    rs2: RuleSet[int] = RuleSet()
    rs2.add_dep(1, 2)
    rs2.add_dep(2, 3)
    rs2.add_dep(3, 4)

    options2: Options[int] = Options(rs2)
    options2.toggle(1)
    print(options2.selected)

"""Usage of options.py and ruleset.py."""

from .options import Options
from .ruleset import RuleSet

if __name__ == "__main__":
    rs: RuleSet[str]=RuleSet()
    rs.add_dep('A', 'B')
    rs.add_dep( "B","C" )
    rs.add_dep("C",    "D")

    options: Options[str] = Options( rs )
    options.toggle("A")
    print(options.selected)
    options.toggle('D')
    print(options.selected)

    rs2: RuleSet[int] = RuleSet()
    rs2.add_dep(1,2)
    rs2.add_dep(2,3)
    rs2.add_dep(3,4)

    options2: Options[int] = Options(rs2)
    options2.toggle(1)
    print(options2.selected)

    rs3: RuleSet[str] = RuleSet()
    deps = [
        ("color",    "terminal"),
        ("unicode",  "terminal"),
        ("terminal", "output"),
    ]
    for a, b in deps:
        rs3.add_dep(a, b)
    rs3.add_conflict(
        "color",
        "plain"
    )
    rs3.add_conflict(
        "unicode",
        "ascii",
    )

    options3: Options[str] = Options(rs3)
    options3.toggle("plain")
    options3.toggle("color")
    print(options3.selected)

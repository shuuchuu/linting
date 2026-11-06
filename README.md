# Typing, defect detection, formatting and automation with `pyrefly`, `ruff` and `pre-commit`

*[Version française](https://github.com/shuuchuu/linting)*

The project of the *Typing, defect detection, formatting and automation* lab. Its
instructions are below, to run the lab in a GitHub Codespace or a local clone; they are
the same as the lab's notebook, in
[English](https://colab.research.google.com/github/shuuchuu/labs/blob/main/linting-hands-on-en.ipynb)
or in
[French](https://colab.research.google.com/github/shuuchuu/labs/blob/main/linting-hands-on-fr.ipynb),
which runs it in Colab.

The `linting` package (in `src/linting/`) manages options that depend on one another:
`ruleset.py` declares the dependencies and the conflicts, `options.py` keeps the
selection up to date, and `code_to_type.py` holds a few functions without type
annotations. The tools are the course's: `ruff` (defects and formatting), `pyrefly`
(types) and `pre-commit` (their automation).

The exercises follow one another: the first, typing, needs only `pyrefly`, then
`pyproject.toml` grows from one to the next, and the last one assumes the previous ones
are done.

## Setting up the working environment

This English version of the lab is the repository's `main-en` branch. Open it in a
Codespace: on GitHub, on the `main-en` branch, **Code** > **Codespaces** > **Create
codespace on main-en**, or [this
link](https://codespaces.new/shuuchuu/linting/tree/main-en). The Codespace installs the
dependencies when it is created, in the project's `.venv`.

In a local clone of that branch, install
[uv](https://docs.astral.sh/uv/getting-started/installation/), then run `uv sync` at the
root of the repository:

```console
git clone -b main-en https://github.com/shuuchuu/linting.git
cd linting
uv sync
```

The commands below run in a terminal at the root of the repository (**Terminal** > **New
Terminal** in the Codespace), through `uv run`, which runs them in the project's
environment, at the versions of `ruff` and `pyrefly` that `uv.lock` pins. The files are
edited in the editor. The solutions are also on the repository's [`solution-en`
branch](https://github.com/shuuchuu/linting/tree/solution-en).

## Typing the functions

The functions of `src/linting/code_to_type.py` have no type annotations. Annotate them,
then check with `uv run pyrefly check` that the annotations agree with the code.
Finally, add an incorrect call, `total(["1", "2"])`, at the end of the `if __name__ ==
"__main__":` block: what does `pyrefly` report, and what does running the module (`uv
run python -m linting.code_to_type`) give? Then remove that call.

**Useful documentation**

- https://docs.python.org/3/library/collections.abc.html
- https://docs.python.org/3/reference/compound_stmts.html#generic-functions

<details>
<summary>Additional hints</summary>

`add` adds two `int`s, `total` iterates over `int`s without needing a list
(`Iterable[int]`), and `upper_keys` only reads a dictionary with `str` keys
(`Mapping[str, ...]`). Its values can be of any type, which the returned dictionary
keeps: a generic function, `def f[T](x: T) -> T`, says so. `Iterable` and `Mapping` are
imported from `collections.abc`. `pyrefly` reports the incorrect call with a
`bad-argument-type` error, which running it confirms with a `TypeError`.

```python
from collections.abc import Iterable, Mapping


def add(a: int, b: int) -> int: ...


def total(numbers: Iterable[int]) -> int: ...


def upper_keys[T](mapping: Mapping[str, T]) -> ...: ...
```

```console
uv run pyrefly check
```

</details>

<details>
<summary>Solution</summary>

`src/linting/code_to_type.py`:

```python
"""Simple code to type."""

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

    Args:
        mapping: Input mapping

    Returns:
        Dictionary with the uppercase keys.
    """
    result = {}
    for key, value in mapping.items():
        result[key.upper()] = value
    return result


if __name__ == "__main__":
    print("add(1, 2) →", add(1, 2))
    print("total([1, 2, 3]) →", total([1, 2, 3]))
    print('upper_keys({"a": 1, "b": 2}) →', upper_keys({"a": 1, "b": 2}))
```

```console
uv run pyrefly check
```

</details>

## Defect detection

Run `uv run ruff check src/linting/options.py`, read each defect it reports (its code,
its line, its suggested fix), then fix them. Which ones can `ruff` fix on its own?

Not everything gets fixed. In `pyproject.toml`, add the `T20` family, which flags
`print` calls, to the `extend-select` list, then run `uv run ruff check`. The `ANN`
rules, which `pyproject.toml` already selects, flag missing annotations: they report
nothing if the first exercise is complete. These `print` calls are intended: exempt the
whole `rules.py` file, which is only a demonstration, and ignore those of
`code_to_type.py` line by line.

**Useful documentation**

- https://docs.astral.sh/ruff/linter/#fixes
- https://docs.astral.sh/ruff/rules/print/

<details>
<summary>Additional hints</summary>

The three defects are an unused import (`F401`), a comparison to `False` (`E712`) and a
membership test written `not x in y` (`E713`). `uv run ruff check --fix` applies the
safe fixes, marked `[*]`; `E712`'s is deemed unsafe (`--unsafe-fixes`), since `x ==
False` and `not x` differ when `x` isn't a boolean.

```python
while not ...:
    ...
    if other_option not in ...:
        ...
```

`ruff` reports 7 `print` calls (`T201`): 4 in `rules.py`, 3 in `code_to_type.py`. The
first file is exempted through `per-file-ignores`, in a
`[tool.ruff.lint.per-file-ignores]` table, and each `print` of the second one gets `#
noqa: T201` at the end of its line.

```toml
[tool.ruff.lint]
extend-select = ["ANN", "E7", "T20"]

[tool.ruff.lint.per-file-ignores]
"src/linting/rules.py" = [...]
```

</details>

<details>
<summary>Solution</summary>

`src/linting/options.py`:

```python
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

        Yields:
            Set of selected options.
        """
        return set(self.selected)

    def remove_dependents(self, options: Iterable[T]) -> None:
        """Remove options and their dependents from the selection.

        Args:
            option: Options from which to compute the dependents to remove.
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
        if option in self.selected:
            self.remove_dependents({option})
        else:
            deps = self.rule_set.compute_deps(option)
            self.remove_dependents(
                set.union(*[self.rule_set.conflicts[d] for d in deps])
            )
            self.selected |= deps
```

`ruff check --fix` fixes the unused import and the `not in` on its own.

`pyproject.toml`:

```toml
[tool.ruff.lint]
extend-select = ["ANN", "E7", "T20"]

[tool.ruff.lint.per-file-ignores]
"src/linting/rules.py" = ["T201"]
```

`ruff` writes the `# noqa: T201` comments of `code_to_type.py` itself; by hand, it's the
same comment.

```console
uv run ruff check --select T20 --add-noqa src/linting/code_to_type.py
uv run ruff check
```

</details>

## Code formatting

Formatting code wastes a lot of time, in code reviews as while writing it. A very
interesting option is to delegate that task entirely to a dedicated tool: in Python,
`ruff` can take care of it. In the Codespace, the editor is already set up to run `ruff
format` on every save.

`src/linting/rules.py` was written by hand, without a formatter: `uv run ruff format
--check` fails. See what `uv run ruff format --diff` suggests changing, and apply it
with `uv run ruff format`. Yet the formatter doesn't decide everything. Read the file
again:

1. Of the two `add_conflict` calls split over several lines, only one stayed that way.
   What sets them apart? Make the other one stay split too.
2. The formatter undid the alignment of the `deps` table, which read as columns. Restore
   it, and protect that statement so that `uv run ruff format --check` passes.

In the Codespace, save the file after restoring the alignment, before protecting it:
what happens?

**Useful documentation**

- https://docs.astral.sh/ruff/formatter/
- https://docs.astral.sh/ruff/formatter/#format-suppression

<details>
<summary>Additional hints</summary>

`--diff` shows the changes without touching the files, and `--check` only says whether
there are any (that's what continuous integration runs). The formatter doesn't change
what the code does: it reindents, restores double quotes and breaks lines longer than 88
characters. It also joins on one line what fits there, unless the last element is
followed by a comma: this trailing comma, known as magic, asks it to keep one element
per line. A `# fmt: skip` comment at the end of a statement, after its last bracket,
makes it leave that statement as it is. `git diff src/linting/rules.py` shows the
original alignment.

```python
deps = [
    ("color",    "terminal"),
    ...
]  # fmt: skip
```

</details>

<details>
<summary>Solution</summary>

```console
uv run ruff format --check
uv run ruff format --diff
uv run ruff format
```

`src/linting/rules.py`:

```python
"""Usage of options.py and ruleset.py."""

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
    options.toggle("D")
    print(options.selected)

    rs2: RuleSet[int] = RuleSet()
    rs2.add_dep(1, 2)
    rs2.add_dep(2, 3)
    rs2.add_dep(3, 4)

    options2: Options[int] = Options(rs2)
    options2.toggle(1)
    print(options2.selected)

    rs3: RuleSet[str] = RuleSet()
    deps = [
        ("color",    "terminal"),
        ("unicode",  "terminal"),
        ("terminal", "output"),
    ]  # fmt: skip
    for a, b in deps:
        rs3.add_dep(a, b)
    rs3.add_conflict(
        "color",
        "plain",
    )
    rs3.add_conflict(
        "unicode",
        "ascii",
    )

    options3: Options[str] = Options(rs3)
    options3.toggle("plain")
    options3.toggle("color")
    print(options3.selected)
```

The call that stayed split has a comma after its last argument, the magic trailing
comma: `ruff format` then keeps one argument per line. For the table, `# fmt: skip`
leaves the statement it ends as it is.

```console
uv run ruff format --check
uv run python -m linting.rules
```

In the Codespace, saving formats the file at once (the `editor.formatOnSave` setting of
`.devcontainer/devcontainer.json`): without `# fmt: skip`, the alignment is gone on the
first save.

</details>

## Detecting overly complex code

`ruff` detects overly complex code from its [cyclomatic
complexity](https://en.wikipedia.org/wiki/Cyclomatic_complexity), the number of
independent paths through a function. In `pyproject.toml`, add the `C901` rule to the
selected rules, and set the option for the maximum complexity allowed to `4`: `uv run
ruff check` then flags a method of `options.py`.

Rewrite that method so that `max-complexity = 4` passes, without changing its result:
the `options.toggle("D")` of `rules.py` must still empty the selection (`uv run python
-m linting.rules` prints `set()` on its second line). Keep that value for the rest of
the lab.

**Useful documentation**

- https://docs.astral.sh/ruff/rules/complex-structure/
- https://docs.astral.sh/ruff/settings/#lint_mccabe_max-complexity

<details>
<summary>Additional hints</summary>

The rule goes in the `extend-select` list of the `[tool.ruff.lint]` table, and the
option is set in a `[tool.ruff.lint.mccabe]` table. `remove_dependents` has a complexity
of 5: a `while` loop, a `for` loop and two nested `if`s. Moving a loop to another method
would make the rule pass without simplifying the code. Look instead at what
`compute_deps` returns: all the dependencies of an option, direct or not, and the option
itself. A single pass over the selection is therefore enough to find the options to
remove: the `while` has no reason to be there.

```python
def remove_dependents(self, options: Iterable[T]) -> None:
    to_remove = set(options)
    self.selected -= {other_option for other_option in self.selected if ...}
```

```toml
[tool.ruff.lint]
extend-select = ["ANN", "C901", "E7", "T20"]

[tool.ruff.lint.mccabe]
max-complexity = ...
```

</details>

<details>
<summary>Solution</summary>

`pyproject.toml`:

```toml
[tool.ruff.lint]
extend-select = ["ANN", "C901", "E7", "T20"]

[tool.ruff.lint.mccabe]
max-complexity = 4

[tool.ruff.lint.per-file-ignores]
"src/linting/rules.py" = ["T201"]
```

`src/linting/options.py`:

```python
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

        Yields:
            Set of selected options.
        """
        return set(self.selected)

    def remove_dependents(self, options: Iterable[T]) -> None:
        """Remove options and their dependents from the selection.

        Args:
            option: Options from which to compute the dependents to remove.
        """
        to_remove = set(options)
        self.selected -= {
            other_option
            for other_option in self.selected
            if to_remove & self.rule_set.compute_deps(other_option)
        }

    def toggle(self, option: T) -> None:
        if option in self.selected:
            self.remove_dependents({option})
        else:
            deps = self.rule_set.compute_deps(option)
            self.remove_dependents(
                set.union(*[self.rule_set.conflicts[d] for d in deps])
            )
            self.selected |= deps
```

`remove_dependents` no longer has a `while` loop, nor nested `if`s.

```console
uv run ruff check
uv run python -m linting.rules
```

</details>

## Documentation quality

Documentation is a very important part of code. To fight documentation drift, its
gradual obsolescence with respect to the code, tooling matters.

In `pyproject.toml`, add the `D` and `DOC` rules to the selected rules, turn on `ruff`'s
*preview* mode (`preview = true`, which the `DOC` rules need) and set the docstring
convention to the `google` style. Then fix the defects that `uv run ruff check` reports.

**Useful documentation**

- https://docs.astral.sh/ruff/settings/#lint_preview
- https://docs.astral.sh/ruff/settings/#lint_pydocstyle_convention

<details>
<summary>Additional hints</summary>

`ruff` reports four defects, all in `options.py`: a `Yields` section in a function that
returns its value (`Returns`), a parameter documented under another name than its own,
the same parameter therefore undocumented, and a public method without a docstring. In
*preview* mode, the report gives each rule's name instead of its code: `uv run ruff rule
docstring-extraneous-yields` gives the code, the one `# noqa` expects.

```toml
[tool.ruff.lint]
preview = true
extend-select = [..., "D", "DOC", ...]

[tool.ruff.lint.pydocstyle]
convention = ...
```

</details>

<details>
<summary>Solution</summary>

`pyproject.toml`:

```toml
[tool.ruff.lint]
preview = true
extend-select = ["ANN", "C901", "D", "DOC", "E7", "T20"]

[tool.ruff.lint.mccabe]
max-complexity = 4

[tool.ruff.lint.per-file-ignores]
"src/linting/rules.py" = ["T201"]

[tool.ruff.lint.pydocstyle]
convention = "google"
```

`src/linting/options.py`:

```python
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
            options: Options from which to compute the dependents to remove.
        """
        to_remove = set(options)
        self.selected -= {
            other_option
            for other_option in self.selected
            if to_remove & self.rule_set.compute_deps(other_option)
        }

    def toggle(self, option: T) -> None:
        """Toggle an option, with its dependencies and dependents.

        Args:
            option: Option to toggle.
        """
        if option in self.selected:
            self.remove_dependents({option})
        else:
            deps = self.rule_set.compute_deps(option)
            self.remove_dependents(
                set.union(*[self.rule_set.conflicts[d] for d in deps])
            )
            self.selected |= deps
```

```console
uv run ruff check
```

</details>

## Automating the checks with `pre-commit`

Rather than counting on everyone to run the checks, run them on every `git commit` with
`pre-commit`. The repository already holds a `.pre-commit-config.yaml` file, with the
`ruff-check`, `ruff-format` and `pyrefly-check` hooks. Its `rev` sets `ruff`'s version a
second time, after `uv.lock`: the two can diverge.

1. Replace the two `ruff` hooks with local hooks (`repo: local`, `language: system`)
   that run `uv run ruff`, so that the version is the one in `uv.lock`. What do you
   gain, what do you lose?
2. Install the git hook with `uvx pre-commit install`, then check the whole repository
   with `uvx pre-commit run --all-files`.
3. Add an unused import and a typing error to `options.py`, then try to commit (`git
   commit -am "Try"`): watch the refusal, and what `ruff` fixed on its own. Then add,
   under the typing error, the line `y: int = "a" # pyrefly: ignore[bad-assignment]`:
   what does `uv run pyrefly check` say about these two lines? Remove them.
4. A hook can be bypassed (`git commit --no-verify`): what command would you run in
   continuous integration to check every pull request anyway?

**Useful documentation**

- https://pre-commit.com/#repository-local-hooks

<details>
<summary>Additional hints</summary>

A local hook is declared under `repo: local`, without a `rev`: `id` and `name` name it,
`entry` is the command to run, to which `pre-commit` adds the files to check, `language:
system` tells it to install nothing, and `types: [python]` to pass Python files only.
`pyrefly-check` doesn't change: `pre-commit` installs it in an environment of its own,
on its first run, and it checks the whole project, without seeing its dependencies (this
one has none). A typing error is for instance `x: int = "a"`. The files `ruff` fixed
during the refused commit are modified but not staged: `git add` stages them.

```yaml
repos:
  - repo: local
    hooks:
      - id: ruff-check
        name: ruff check
        entry: uv run ruff check --fix
        language: system
        types: [python]
      - id: ...
  - repo: https://github.com/meta/pyrefly-pre-commit
    rev: 1.4.0
    hooks:
      - id: pyrefly-check
```

</details>

<details>
<summary>Solution</summary>

`.pre-commit-config.yaml`:

```yaml
repos:
  - repo: local
    hooks:
      - id: ruff-check
        name: ruff check
        entry: uv run ruff check --fix
        language: system
        types: [python]
      - id: ruff-format
        name: ruff format
        entry: uv run ruff format
        language: system
        types: [python]
  - repo: https://github.com/meta/pyrefly-pre-commit
    rev: 1.4.0
    hooks:
      - id: pyrefly-check
```

Local hooks gain a single version of `ruff`, the one in `uv.lock`, for the hook, the
command line and continuous integration, and no more `rev` to keep up to date. They
lose the isolation: each machine needs `uv` and the project's environment, and
`pre-commit autoupdate` no longer follows them.

```console
uvx pre-commit install
uvx pre-commit run --all-files
git add --all
git commit -m "Check the code on every commit"
```

After adding an unused import and `x: int = "a"` to `options.py`, `git commit -am "Try"`
is refused: `ruff-check` removed the import (the file is modified, to stage again), and
`pyrefly` reports the typing error (`bad-assignment`), to fix by hand. With the ignored
line as well, `uv run pyrefly check` says `1 error (1 suppressed)`.

In continuous integration, `uvx pre-commit run --all-files` runs the same hooks on the
whole repository, and fails if one of them fails, whether `--no-verify` was used or
not. The commands `uv run ruff check`, `uv run ruff format --check` and `uv run pyrefly
check` work too: they fix nothing, where the hook runs `--fix`, and `pyrefly` runs at
the version in `uv.lock`, with the project's dependencies.

</details>

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

The functions of `src/linting/code_to_type.py` have no type annotations. `ruff`'s `ANN`
rules, which `pyproject.toml` selects, flag every parameter and every return value
without one: run `uv run ruff check src/linting/code_to_type.py`.

Annotate the three functions until `ruff` flags nothing in that file any more, then
check with `uv run pyrefly check` that the annotations agree with the code. Finally, add an
incorrect call, `total(["1", "2"])`, at the end of the `if __name__ == "__main__":`
block: what does `pyrefly` report, and what does running the module (`uv run python -m
linting.code_to_type`) give? Then remove that call.

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

    Params:
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
uv run ruff check src/linting/code_to_type.py
uv run pyrefly check
```

</details>

## Defect detection

Run `uv run ruff check src/linting/options.py`, read each defect it reports (its code,
its line, its suggested fix), then fix them. Which ones can `ruff` fix on its own?

**Useful documentation**

- https://docs.astral.sh/ruff/linter/#fixes

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

```console
uv run ruff check src/linting/options.py
```

</details>

## Detecting overly complex code

`ruff` detects overly complex code from its [cyclomatic
complexity](https://en.wikipedia.org/wiki/Cyclomatic_complexity), the number of
independent paths through a function. In `pyproject.toml`, add the `C901` rule to the
selected rules, and give a value to the option that sets the maximum complexity
allowed. What is the largest value for which `uv run ruff check` reports an error, and
on which function? Look at it, then set the option to `10` for the rest of the lab.

**Useful documentation**

- https://docs.astral.sh/ruff/rules/complex-structure/
- https://docs.astral.sh/ruff/settings/#lint_mccabe_max-complexity

<details>
<summary>Additional hints</summary>

The rule goes in the `select` list of the `[tool.ruff.lint]` table, and the option is
set in a `[tool.ruff.lint.mccabe]` table. Start from `1`, which flags every function
with at least one `if` or loop, and increase it: the message gives the complexity of
each function it flags.

```toml
[tool.ruff.lint]
select = ["ANN", "C901", "E4", "E7", "E9", "F", "I"]

[tool.ruff.lint.mccabe]
max-complexity = 1
```

</details>

<details>
<summary>Solution</summary>

Up to `max-complexity = 4`, `ruff` flags `remove_dependents`, in `options.py`, of
complexity 5: a `while` loop, a `for` loop and two nested `if`s. `pyproject.toml`,
then:

```toml
[tool.ruff.lint]
select = ["ANN", "C901", "E4", "E7", "E9", "F", "I"]

[tool.ruff.lint.mccabe]
# `remove_dependents` (complexity 5) is flagged up to a maximum of 4.
max-complexity = 10
```

```console
uv run ruff check
```

</details>

## Code formatting

Formatting code wastes a lot of time, in code reviews as while writing it. A very
interesting option is to delegate that task entirely to a dedicated tool: in Python,
`ruff` can take care of it. In the Codespace, the editor is already set to run `ruff
format` on every save.

Degrade the layout of `src/linting/rules.py` (extra spaces around an `=`, single quotes,
a long line), then see what `uv run ruff format --diff` suggests changing, and apply it
with `uv run ruff format`. In the Codespace, also save the modified file: what happens?

**Useful documentation**

- https://docs.astral.sh/ruff/formatter/

<details>
<summary>Additional hints</summary>

`--diff` shows the changes without touching the files, and `--check` only says whether
there are any (that's what continuous integration runs). The formatter doesn't change
what the code does: it reindents, restores double quotes and breaks lines longer than
88 characters.

```text
rs: RuleSet[str]=RuleSet()
rs.add_dep('A', 'B')
```

</details>

<details>
<summary>Solution</summary>

```console
uv run ruff format --diff
uv run ruff format
uv run ruff format --check
```

In the Codespace, saving formats the file at once (the `editor.formatOnSave` setting of
`.devcontainer/devcontainer.json`).

</details>

## Documentation quality

Documentation is a very important part of code. To fight documentation drift, its
gradual obsolescence with respect to the code, tooling matters.

In `pyproject.toml`, add the `D` and `DOC` rules to the selected rules, turn on `ruff`'s
*preview* mode (`preview = true`, which the `DOC` rules need) and set the docstring
convention to the `google` style. Then fix the defects that `uv run ruff check`
reports.

**Useful documentation**

- https://docs.astral.sh/ruff/settings/#lint_preview
- https://docs.astral.sh/ruff/settings/#lint_pydocstyle_convention

<details>
<summary>Additional hints</summary>

`ruff` reports four defects, all in `options.py`: a `Yields` section in a function that
returns its value (`Returns`), a parameter documented under another name than its own,
the same parameter therefore undocumented, and a public method without a docstring.

```toml
[tool.ruff.lint]
preview = true
select = [..., "D", "DOC", ...]

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
select = ["ANN", "C901", "D", "DOC", "E4", "E7", "E9", "F", "I"]

[tool.ruff.lint.mccabe]
# `remove_dependents` (complexity 5) is flagged up to a maximum of 4.
max-complexity = 10

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
`pre-commit`:

1. At the repository's root, create a `.pre-commit-config.yaml` file declaring the
   `ruff-check` (with the `--fix` argument) and `ruff-format` hooks of the
   `ruff-pre-commit` repository, and the `pyrefly-check` hook of the `pyrefly-pre-commit`
   repository, at the versions (`rev`) of `ruff` and `pyrefly` you use.
2. Install the git hook with `uvx pre-commit install`, then check the whole repository
   with `uvx pre-commit run --all-files`.
3. Add an unused import and a typing error to `options.py`, then try to commit: watch
   the refusal, and what `ruff` fixed on its own.
4. A hook can be bypassed (`git commit --no-verify`): what command would you run in
   continuous integration to check every pull request anyway?

**Useful documentation**

- https://github.com/astral-sh/ruff-pre-commit
- https://github.com/facebook/pyrefly-pre-commit

<details>
<summary>Additional hints</summary>

`uv run ruff --version` and `uv run pyrefly --version` give the versions: the `ruff`
hook's `rev` is its version's tag, prefixed with a `v`, the `pyrefly` hook's its version
as is. `pre-commit` installs each hook in an environment of its own, on its first run;
`pyrefly-check` checks the whole project, without seeing its dependencies (this one has
none). A typing error is for instance `x: int =
"a"`. The files `ruff` fixed during the refused commit are modified but not staged:
`git add` stages them.

```yaml
repos:
  - repo: https://github.com/astral-sh/ruff-pre-commit
    rev: v...
    hooks:
      - id: ruff-check
        args: [--fix]
      - id: ...
  - repo: https://github.com/facebook/pyrefly-pre-commit
    rev: ...
    hooks:
      - id: pyrefly-check
```

</details>

<details>
<summary>Solution</summary>

`.pre-commit-config.yaml`:

```yaml
repos:
  - repo: https://github.com/astral-sh/ruff-pre-commit
    rev: v0.17.1
    hooks:
      - id: ruff-check
        args: [--fix]
      - id: ruff-format
  - repo: https://github.com/facebook/pyrefly-pre-commit
    rev: 1.4.0
    hooks:
      - id: pyrefly-check
```

```console
uvx pre-commit install
uvx pre-commit run --all-files
git add --all
git commit -m "Check the code on every commit"
```

After adding an unused import and `x: int = "a"` to `options.py`, `git commit -am "Try"`
is refused: `ruff-check` removed the import (the file is modified, to stage again), and
`pyrefly` reports the typing error (`bad-assignment`), to fix by hand.

In continuous integration, `uvx pre-commit run --all-files` runs the same hooks on the
whole repository, and fails if one of them fails, whether the commit used `--no-verify`
or not.

</details>

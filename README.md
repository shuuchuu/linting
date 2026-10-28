# Typage, détection de défauts, formatage et automatisation avec `pyrefly`, `ruff` et `pre-commit`

*[English version](https://github.com/shuuchuu/linting/tree/main-en)*

Le projet des travaux pratiques *Typage, détection de défauts, formatage et
automatisation*. Leur énoncé est ci-dessous, pour les faire dans un Codespace GitHub ou
un clone local&nbsp;; c'est le même que celui du notebook des travaux pratiques, en
[français](https://colab.research.google.com/github/shuuchuu/labs/blob/main/linting-hands-on-fr.ipynb)
ou en
[anglais](https://colab.research.google.com/github/shuuchuu/labs/blob/main/linting-hands-on-en.ipynb),
qui les fait dans Colab.

Le paquet `linting` (dans `src/linting/`) gère des options qui dépendent les unes des
autres&nbsp;: `ruleset.py` déclare les dépendances et les conflits, `options.py` tient
la sélection à jour, et `code_to_type.py` réunit quelques fonctions sans annotations de
type. Les outils sont ceux du cours&nbsp;: `ruff` (défauts et formatage), `pyrefly`
(types) et `pre-commit` (leur automatisation).

## Mise en place de l'environnement de travail

Ouvrez le dépôt dans un Codespace&nbsp;: sur GitHub, **Code** > **Codespaces** >
**Create codespace on main**, ou [ce lien](https://codespaces.new/shuuchuu/linting). Le
Codespace installe les dépendances à sa création, dans le `.venv` du projet.

Dans un clone local, installez
[uv](https://docs.astral.sh/uv/getting-started/installation/), puis lancez `uv sync` à
la racine du dépôt.

Les commandes ci-dessous se lancent dans un terminal à la racine du dépôt (**Terminal** >
**Nouveau terminal** dans le Codespace), avec `uv run`, qui les exécute dans
l'environnement du projet, aux versions de `ruff` et `pyrefly` que fixe `uv.lock`. Les
fichiers se modifient dans l'éditeur. Les solutions sont aussi sur la [branche
`solution`](https://github.com/shuuchuu/linting/tree/solution) du dépôt.

## Typage des fonctions

Les fonctions de `src/linting/code_to_type.py` n'ont pas d'annotations de type. Les
règles `ANN` de `ruff`, que `pyproject.toml` sélectionne, signalent chaque paramètre et
chaque valeur de retour sans annotation&nbsp;: lancez `uv run ruff check
src/linting/code_to_type.py`.

Annotez les trois fonctions jusqu'à ce que `ruff` ne signale plus rien dans ce fichier,
puis vérifiez avec `uv run pyrefly check` que les annotations sont cohérentes avec le code.
Ajoutez enfin, à la fin du bloc `if __name__ == "__main__":`, un appel incorrect,
`total(["1", "2"])`&nbsp;: que signale `pyrefly`, et que donne l'exécution du module (`uv run
python -m linting.code_to_type`)&nbsp;? Retirez ensuite cet appel.

**Documentation utile**

- https://docs.python.org/fr/3/library/collections.abc.html
- https://docs.python.org/fr/3/reference/compound_stmts.html#generic-functions

<details>
<summary>Conseils supplémentaires</summary>

`add` additionne deux `int`, `total` parcourt des `int` sans avoir besoin d'une liste
(`Iterable[int]`), et `upper_keys` ne fait que lire un dictionnaire aux clés `str`
(`Mapping[str, ...]`). Ses valeurs peuvent être de n'importe quel type, que le
dictionnaire renvoyé conserve&nbsp;: une fonction générique, `def f[T](x: T) -> T`, le
dit. `Iterable` et `Mapping` s'importent de `collections.abc`. `pyrefly` signale l'appel
incorrect par une erreur `bad-argument-type`, que l'exécution confirme par une
`TypeError`.

```python
from collections.abc import Iterable, Mapping


def add(a: int, b: int) -> int: ...


def total(numbers: Iterable[int]) -> int: ...


def upper_keys[T](mapping: Mapping[str, T]) -> ...: ...
```

</details>

<details>
<summary>Solution</summary>

`src/linting/code_to_type.py`&nbsp;:

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

## Détection de défauts

Lancez `uv run ruff check src/linting/options.py`, lisez chaque défaut signalé (son
code, sa ligne, sa correction proposée), puis corrigez-les. Lesquels `ruff` sait-il
corriger seul&nbsp;?

**Documentation utile**

- https://docs.astral.sh/ruff/linter/#fixes

<details>
<summary>Conseils supplémentaires</summary>

Les trois défauts sont un import inutilisé (`F401`), une comparaison à `False` (`E712`)
et un test d'appartenance écrit `not x in y` (`E713`). `uv run ruff check --fix`
applique les corrections sûres, marquées `[*]`&nbsp;; celle de `E712` est dite
dangereuse (`--unsafe-fixes`), car `x == False` et `not x` diffèrent quand `x` n'est
pas un booléen.

```python
while not ...:
    ...
    if other_option not in ...:
        ...
```

</details>

<details>
<summary>Solution</summary>

`src/linting/options.py`&nbsp;:

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

`ruff check --fix` corrige seul l'import inutilisé et le `not in`.

```console
uv run ruff check src/linting/options.py
```

</details>

## Détection de code trop complexe

`ruff` détecte le code trop complexe d'après sa [complexité
cyclomatique](https://fr.wikipedia.org/wiki/Nombre_cyclomatique), le nombre de chemins
indépendants dans une fonction. Dans `pyproject.toml`, ajoutez la règle `C901` aux
règles sélectionnées, et donnez une valeur à l'option qui fixe la complexité maximale
admise. Quelle est la plus grande valeur pour laquelle `uv run ruff check` signale une
erreur, et sur quelle fonction&nbsp;? Observez-la, puis fixez l'option à `10` pour la
suite des travaux pratiques.

**Documentation utile**

- https://docs.astral.sh/ruff/rules/complex-structure/
- https://docs.astral.sh/ruff/settings/#lint_mccabe_max-complexity

<details>
<summary>Conseils supplémentaires</summary>

La règle s'ajoute à la liste `select` de la table `[tool.ruff.lint]`, et l'option se
règle dans une table `[tool.ruff.lint.mccabe]`. Partez de `1`, qui signale toutes les
fonctions qui ont au moins un `if` ou une boucle, et augmentez&nbsp;: le message donne
la complexité de chaque fonction signalée.

```toml
[tool.ruff.lint]
select = ["ANN", "C901", "E4", "E7", "E9", "F", "I"]

[tool.ruff.lint.mccabe]
max-complexity = 1
```

</details>

<details>
<summary>Solution</summary>

Jusqu'à `max-complexity = 4`, `ruff` signale `remove_dependents`, dans `options.py`, de
complexité 5&nbsp;: une boucle `while`, une boucle `for` et deux `if` imbriqués.
`pyproject.toml`, ensuite&nbsp;:

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

## Formatage du code

Le formatage du code fait perdre beaucoup de temps, en revue de code comme pendant
l'écriture. Une option très intéressante est de déléguer complètement cette tâche à un
outil dédié&nbsp;: en Python, `ruff` peut s'en charger. Dans le Codespace, l'éditeur est
déjà configuré pour lancer `ruff format` à chaque sauvegarde.

Dégradez la mise en forme de `src/linting/rules.py` (des espaces en trop autour d'un
`=`, des guillemets simples, une longue ligne), puis voyez ce que `uv run ruff format
--diff` propose de changer, et appliquez-le avec `uv run ruff format`. Dans le
Codespace, sauvegardez aussi le fichier modifié&nbsp;: que se passe-t-il&nbsp;?

**Documentation utile**

- https://docs.astral.sh/ruff/formatter/

<details>
<summary>Conseils supplémentaires</summary>

`--diff` affiche les changements sans toucher aux fichiers, et `--check` dit seulement
s'il y en a (c'est ce qu'on lance en intégration continue). Le formateur ne change pas
ce que fait le code&nbsp;: il réindente, remet les guillemets doubles et coupe les
lignes de plus de 88 caractères.

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

Dans le Codespace, la sauvegarde formate le fichier aussitôt (le réglage
`editor.formatOnSave` de `.devcontainer/devcontainer.json`).

</details>

## Qualité de la documentation

La documentation est une partie très importante du code. Pour lutter contre la dérive de
la documentation, son obsolescence progressive par rapport au code, il est important de
s'outiller.

Dans `pyproject.toml`, ajoutez les règles `D` et `DOC` aux règles sélectionnées,
activez le mode *preview* de `ruff` (`preview = true`, dont les règles `DOC` ont besoin)
et configurez le style des docstrings pour utiliser le style `google`. Corrigez ensuite
les défauts que `uv run ruff check` relève.

**Documentation utile**

- https://docs.astral.sh/ruff/settings/#lint_preview
- https://docs.astral.sh/ruff/settings/#lint_pydocstyle_convention

<details>
<summary>Conseils supplémentaires</summary>

`ruff` relève quatre défauts, tous dans `options.py`&nbsp;: une section `Yields` dans
une fonction qui renvoie sa valeur (`Returns`), un paramètre documenté sous un autre nom
que le sien, le même paramètre donc non documenté, et une méthode publique sans
docstring.

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

`pyproject.toml`&nbsp;:

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

`src/linting/options.py`&nbsp;:

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

## Automatisation des vérifications avec `pre-commit`

Plutôt que de compter sur chacun pour lancer les vérifications, faites-les tourner à
chaque `git commit` avec `pre-commit`&nbsp;:

1. Créez à la racine du dépôt un fichier `.pre-commit-config.yaml` qui déclare les hooks
   `ruff-check` (avec l'argument `--fix`) et `ruff-format` du dépôt `ruff-pre-commit`,
   et le hook `pyrefly-check` du dépôt `pyrefly-pre-commit`, aux versions (`rev`) de
   `ruff` et `pyrefly` que vous utilisez.
2. Installez le hook git avec `uvx pre-commit install`, puis vérifiez tout le dépôt avec
   `uvx pre-commit run --all-files`.
3. Ajoutez à `options.py` un import inutilisé et une erreur de typage, puis essayez de
   commiter&nbsp;: observez le refus, et ce que `ruff` a corrigé seul.
4. Un hook se contourne (`git commit --no-verify`)&nbsp;: quelle commande lanceriez-vous
   en intégration continue pour vérifier quand même chaque *pull request*&nbsp;?

**Documentation utile**

- https://github.com/astral-sh/ruff-pre-commit
- https://github.com/facebook/pyrefly-pre-commit

<details>
<summary>Conseils supplémentaires</summary>

`uv run ruff --version` et `uv run pyrefly --version` donnent les versions&nbsp;: la
`rev` du hook de `ruff` est le tag de sa version, préfixé d'un `v`, celle du hook de
`pyrefly` sa version telle quelle. `pre-commit` installe chaque hook dans un
environnement à lui, au premier lancement&nbsp;; `pyrefly-check` vérifie tout le projet,
sans en voir les dépendances (celui-ci n'en a pas). Une erreur de typage s'obtient par exemple avec `x: int = "a"`. Les fichiers que `ruff` a corrigés pendant
le commit refusé sont modifiés mais pas indexés&nbsp;: `git add` les ajoute.

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

`.pre-commit-config.yaml`&nbsp;:

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
git commit -m "Vérifier le code à chaque commit"
```

Après l'ajout d'un import inutilisé et de `x: int = "a"` à `options.py`, `git commit -am
"Essai"` est refusé&nbsp;: `ruff-check` a retiré l'import (le fichier est modifié, à
indexer de nouveau), et `pyrefly` signale l'erreur de typage (`bad-assignment`), qu'il
faut corriger à la main.

En intégration continue, `uvx pre-commit run --all-files` lance les mêmes hooks sur
tout le dépôt, et échoue si l'un d'eux échoue, qu'on ait commité avec `--no-verify` ou
non.

</details>

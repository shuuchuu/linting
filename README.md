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
autres&nbsp;: `regles.py` déclare les dépendances et les conflits, `options.py` tient la
sélection à jour, et `code_a_typer.py` réunit quelques fonctions sans annotations de
type. Les outils sont ceux du cours&nbsp;: `ruff` (défauts et formatage), `pyrefly`
(types) et `pre-commit` (leur automatisation).

Les exercices se suivent&nbsp;: le premier, le typage, ne demande que `pyrefly`, puis
`pyproject.toml` s'enrichit de l'un à l'autre, et le dernier suppose les précédents
faits.

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

Les fonctions de `src/linting/code_a_typer.py` n'ont pas d'annotations de type.
Annotez-les, puis vérifiez avec `uv run pyrefly check` que les annotations sont
cohérentes avec le code. Ajoutez enfin, à la fin du bloc `if __name__ == "__main__":`,
un appel incorrect, `totalise(["1", "2"])`&nbsp;: que signale `pyrefly`, et que donne
l'exécution du module (`uv run python -m linting.code_a_typer`)&nbsp;? Retirez ensuite
cet appel.

**Documentation utile**

- https://docs.python.org/fr/3/library/collections.abc.html
- https://docs.python.org/fr/3/reference/compound_stmts.html#generic-functions

<details>
<summary>Conseils supplémentaires</summary>

`additionne` additionne deux `int`, `totalise` parcourt des `int` sans avoir besoin
d'une liste (`Iterable[int]`), et `met_en_majuscules` ne fait que lire un dictionnaire
aux clés `str` (`Mapping[str, ...]`). Ses valeurs peuvent être de n'importe quel type,
que le dictionnaire renvoyé conserve&nbsp;: une fonction générique,
`def f[T](x: T) -> T`, le dit. `Iterable` et `Mapping` s'importent de `collections.abc`.
`pyrefly` signale l'appel incorrect par une erreur `bad-argument-type`, que l'exécution
confirme par une `TypeError`.

```python
from collections.abc import Iterable, Mapping


def additionne(a: int, b: int) -> int: ...


def totalise(nombres: Iterable[int]) -> int: ...


def met_en_majuscules[T](dictionnaire: Mapping[str, T]) -> ...: ...
```

```console
uv run pyrefly check
```

</details>

<details>
<summary>Solution</summary>

`src/linting/code_a_typer.py`&nbsp;:

```python
"""Code simple à typer."""

from collections.abc import Iterable, Mapping


def additionne(a: int, b: int) -> int:
    """Calcule la somme de deux nombres.

    Args:
        a: Premier nombre
        b: Deuxième nombre

    Returns:
        Somme des deux nombres.
    """
    return a + b


def totalise(nombres: Iterable[int]) -> int:
    """Calcule la somme d'un itérable de nombres.

    Args:
        nombres: Itérable de nombres

    Returns:
        Somme des nombres.
    """
    total = 0
    for nombre in nombres:
        total += nombre
    return total


def met_en_majuscules[T](dictionnaire: Mapping[str, T]) -> dict[str, T]:
    """Crée un dictionnaire aux clés en majuscules à partir d'un dictionnaire donné.

    Args:
        dictionnaire: Dictionnaire d'entrée

    Returns:
        Dictionnaire aux clés en majuscules.
    """
    resultat = {}
    for cle, valeur in dictionnaire.items():
        resultat[cle.upper()] = valeur
    return resultat


if __name__ == "__main__":
    print("additionne(1, 2) →", additionne(1, 2))
    print("totalise([1, 2, 3]) →", totalise([1, 2, 3]))
    print('met_en_majuscules({"a": 1, "b": 2}) →', met_en_majuscules({"a": 1, "b": 2}))
```

```console
uv run pyrefly check
```

</details>

## Détection de défauts

Lancez `uv run ruff check src/linting/options.py`, lisez chaque défaut signalé (son
code, sa ligne, sa correction proposée), puis corrigez-les. Lesquels `ruff` sait-il
corriger seul&nbsp;?

Tout ne se corrige pas. Dans `pyproject.toml`, ajoutez à la liste `extend-select` la
famille `T20`, qui signale les `print`, puis lancez `uv run ruff check`. Les règles
`ANN`, que `pyproject.toml` sélectionne déjà, signalent les annotations
manquantes&nbsp;: elles ne relèvent rien si le premier exercice est complet. Ces `print`
sont voulus&nbsp;: exemptez-en tout le fichier `demo.py`, qui n'est qu'une
démonstration, et ignorez ceux de `code_a_typer.py` ligne par ligne.

**Documentation utile**

- https://docs.astral.sh/ruff/linter/#fixes
- https://docs.astral.sh/ruff/rules/print/

<details>
<summary>Conseils supplémentaires</summary>

Les trois défauts sont un import inutilisé (`F401`), une comparaison à `False` (`E712`)
et un test d'appartenance écrit `not x in y` (`E713`). `uv run ruff check --fix`
applique les corrections sûres, marquées `[*]`&nbsp;; celle de `E712` est dite
dangereuse (`--unsafe-fixes`), car `x == False` et `not x` diffèrent quand `x` n'est pas
un booléen.

```python
while not ...:
    ...
    if autre_option not in ...:
        ...
```

`ruff` relève 7 `print` (`T201`)&nbsp;: 4 dans `demo.py`, 3 dans `code_a_typer.py`. Le
premier fichier s'exempte par `per-file-ignores`, dans une table
`[tool.ruff.lint.per-file-ignores]`, et chaque `print` du second reçoit `# noqa: T201`
en fin de ligne.

```toml
[tool.ruff.lint]
extend-select = ["ANN", "E7", "T20"]

[tool.ruff.lint.per-file-ignores]
"src/linting/demo.py" = [...]
```

</details>

<details>
<summary>Solution</summary>

`src/linting/options.py`&nbsp;:

```python
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
        while not termine:
            termine = True
            for autre_option in self.selectionnees:
                if a_retirer & self.jeu_regles.calcule_dependances(autre_option):
                    if autre_option not in a_retirer:
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
```

`ruff check --fix` corrige seul l'import inutilisé et le `not in`.

`pyproject.toml`&nbsp;:

```toml
[tool.ruff.lint]
extend-select = ["ANN", "E7", "T20"]

[tool.ruff.lint.per-file-ignores]
"src/linting/demo.py" = ["T201"]
```

`ruff` écrit lui-même les `# noqa: T201` de `code_a_typer.py`&nbsp;; à la main, c'est le
même commentaire.

```console
uv run ruff check --select T20 --add-noqa src/linting/code_a_typer.py
uv run ruff check
```

</details>

## Formatage du code

Le formatage du code fait perdre beaucoup de temps, en revue de code comme pendant
l'écriture. Une option très intéressante est de déléguer complètement cette tâche à un
outil dédié&nbsp;: en Python, `ruff` peut s'en charger. Dans le Codespace, l'éditeur est
déjà configuré pour lancer `ruff format` à chaque sauvegarde.

`src/linting/demo.py` a été écrit à la main, sans formateur&nbsp;: `uv run ruff format
--check` échoue. Voyez ce que `uv run ruff format --diff` propose de changer, et
appliquez-le avec `uv run ruff format`. Le formateur ne décide pourtant pas de tout.
Relisez le fichier&nbsp;:

1. Des deux appels à `ajoute_conflit` coupés sur plusieurs lignes, un seul l'est resté.
   Qu'est-ce qui les distingue&nbsp;? Faites que l'autre le reste aussi.
2. Le formateur a défait l'alignement de la table `dependances`, qui se lisait en
   colonnes. Rétablissez-le, et protégez cette instruction pour que
   `uv run ruff format --check` passe.

Dans le Codespace, sauvegardez le fichier après avoir rétabli l'alignement, sans le
protéger d'abord&nbsp;: que se passe-t-il&nbsp;?

**Documentation utile**

- https://docs.astral.sh/ruff/formatter/
- https://docs.astral.sh/ruff/formatter/#format-suppression

<details>
<summary>Conseils supplémentaires</summary>

`--diff` affiche les changements sans toucher aux fichiers, et `--check` dit seulement
s'il y en a (c'est ce qu'on lance en intégration continue). Le formateur ne change pas
ce que fait le code&nbsp;: il réindente, remet les guillemets doubles et coupe les
lignes de plus de 88 caractères. Il rejoint aussi sur une ligne ce qui y tient, sauf si
le dernier élément est suivi d'une virgule&nbsp;: cette virgule finale, dite magique,
lui demande de garder un élément par ligne. Un commentaire `# fmt: skip` à la fin d'une
instruction, après son dernier crochet, lui fait laisser celle-ci telle quelle. `git
diff src/linting/demo.py` montre l'alignement d'origine.

```python
dependances = [
    ("couleur",  "terminal"),
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

`src/linting/demo.py`&nbsp;:

```python
"""Utilisation de options.py et regles.py."""

from .options import Options
from .regles import JeuRegles

if __name__ == "__main__":
    jeu: JeuRegles[str] = JeuRegles()
    jeu.ajoute_dependance("A", "B")
    jeu.ajoute_dependance("B", "C")
    jeu.ajoute_dependance("C", "D")

    options: Options[str] = Options(jeu)
    options.bascule("A")
    print(options.selectionnees)
    options.bascule("D")
    print(options.selectionnees)

    jeu2: JeuRegles[int] = JeuRegles()
    jeu2.ajoute_dependance(1, 2)
    jeu2.ajoute_dependance(2, 3)
    jeu2.ajoute_dependance(3, 4)

    options2: Options[int] = Options(jeu2)
    options2.bascule(1)
    print(options2.selectionnees)

    jeu3: JeuRegles[str] = JeuRegles()
    dependances = [
        ("couleur",  "terminal"),
        ("unicode",  "terminal"),
        ("terminal", "sortie"),
    ]  # fmt: skip
    for a, b in dependances:
        jeu3.ajoute_dependance(a, b)
    jeu3.ajoute_conflit(
        "couleur",
        "brut",
    )
    jeu3.ajoute_conflit(
        "unicode",
        "ascii",
    )

    options3: Options[str] = Options(jeu3)
    options3.bascule("brut")
    options3.bascule("couleur")
    print(options3.selectionnees)
```

L'appel resté coupé a une virgule après son dernier argument, la virgule finale
magique&nbsp;: `ruff format` garde alors un argument par ligne. Pour la table, `# fmt:
skip` laisse telle quelle l'instruction qu'il termine.

```console
uv run ruff format --check
uv run python -m linting.demo
```

Dans le Codespace, la sauvegarde formate le fichier aussitôt (le réglage
`editor.formatOnSave` de `.devcontainer/devcontainer.json`)&nbsp;: sans `# fmt: skip`,
l'alignement disparaît dès qu'on sauvegarde.

</details>

## Détection de code trop complexe

`ruff` détecte le code trop complexe d'après sa [complexité
cyclomatique](https://fr.wikipedia.org/wiki/Nombre_cyclomatique), le nombre de chemins
indépendants dans une fonction. Dans `pyproject.toml`, ajoutez la règle `C901` aux
règles sélectionnées, et fixez à `4` l'option qui règle la complexité maximale
admise&nbsp;: `uv run ruff check` signale alors une méthode de
`options.py`.

Réécrivez cette méthode pour que `max-complexity = 4` passe, sans changer son
résultat&nbsp;: le `options.bascule("D")` de `demo.py` doit toujours vider la sélection
(`uv run python -m linting.demo` affiche `set()` en deuxième ligne). Gardez cette valeur
pour la suite des travaux pratiques.

**Documentation utile**

- https://docs.astral.sh/ruff/rules/complex-structure/
- https://docs.astral.sh/ruff/settings/#lint_mccabe_max-complexity

<details>
<summary>Conseils supplémentaires</summary>

La règle s'ajoute à la liste `extend-select` de la table `[tool.ruff.lint]`, et l'option
se règle dans une table `[tool.ruff.lint.mccabe]`. `retire_dependants` a une complexité
de 5&nbsp;: une boucle `while`, une boucle `for` et deux `if` imbriqués. Déplacer une
boucle dans une autre méthode ferait passer la règle sans simplifier le code. Regardez
plutôt ce que renvoie `calcule_dependances`&nbsp;: toutes les dépendances d'une option,
directes ou non, et l'option elle-même. Une seule lecture de la sélection suffit donc à
trouver les options à retirer&nbsp;: le `while` n'a pas lieu d'être.

```python
def retire_dependants(self, options: Iterable[T]) -> None:
    a_retirer = set(options)
    self.selectionnees -= {autre_option for autre_option in self.selectionnees if ...}
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

`pyproject.toml`&nbsp;:

```toml
[tool.ruff.lint]
extend-select = ["ANN", "C901", "E7", "T20"]

[tool.ruff.lint.mccabe]
max-complexity = 4

[tool.ruff.lint.per-file-ignores]
"src/linting/demo.py" = ["T201"]
```

`src/linting/options.py`&nbsp;:

```python
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
        self.selectionnees -= {
            autre_option
            for autre_option in self.selectionnees
            if a_retirer & self.jeu_regles.calcule_dependances(autre_option)
        }

    def bascule(self, option: T) -> None:
        if option in self.selectionnees:
            self.retire_dependants({option})
        else:
            dependances = self.jeu_regles.calcule_dependances(option)
            self.retire_dependants(
                set.union(*[self.jeu_regles.conflits[d] for d in dependances])
            )
            self.selectionnees |= dependances
```

`retire_dependants` n'a plus de boucle `while`, ni de `if` imbriqués.

```console
uv run ruff check
uv run python -m linting.demo
```

</details>

## Qualité de la documentation

La documentation est une partie très importante du code. Pour lutter contre la dérive de
la documentation, son obsolescence progressive par rapport au code, il est important de
s'outiller.

Dans `pyproject.toml`, ajoutez les règles `D` et `DOC` aux règles sélectionnées, activez
le mode *preview* de `ruff` (`preview = true`, dont les règles `DOC` ont besoin) et
configurez le style des docstrings pour utiliser le style `google`. Corrigez ensuite les
défauts que `uv run ruff check` relève.

**Documentation utile**

- https://docs.astral.sh/ruff/settings/#lint_preview
- https://docs.astral.sh/ruff/settings/#lint_pydocstyle_convention

<details>
<summary>Conseils supplémentaires</summary>

`ruff` relève quatre défauts, tous dans `options.py`&nbsp;: une section `Yields` dans
une fonction qui renvoie sa valeur (`Returns`), un paramètre documenté sous un autre nom
que le sien, le même paramètre donc non documenté, et une méthode publique sans
docstring. En mode *preview*, le rapport donne le nom de chaque règle au lieu de son
code&nbsp;: `uv run ruff rule docstring-extraneous-yields` donne le code, celui
qu'attend `# noqa`.

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

`pyproject.toml`&nbsp;:

```toml
[tool.ruff.lint]
preview = true
extend-select = ["ANN", "C901", "D", "DOC", "E7", "T20"]

[tool.ruff.lint.mccabe]
max-complexity = 4

[tool.ruff.lint.per-file-ignores]
"src/linting/demo.py" = ["T201"]

[tool.ruff.lint.pydocstyle]
convention = "google"
```

`src/linting/options.py`&nbsp;:

```python
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
```

```console
uv run ruff check
```

</details>

## Automatisation des vérifications avec `pre-commit`

Plutôt que de compter sur chacun pour lancer les vérifications, faites-les tourner à
chaque `git commit` avec `pre-commit`. Le dépôt contient déjà un fichier
`.pre-commit-config.yaml`, avec les hooks `ruff-check`, `ruff-format` et
`pyrefly-check`. Sa `rev` fixe une deuxième fois la version de `ruff`, que `uv.lock`
fixe déjà&nbsp;: les deux peuvent diverger.

1. Remplacez les deux hooks `ruff` par des hooks locaux (`repo: local`, `language:
   system`) qui lancent `uv run ruff`, pour que la version soit celle de `uv.lock`. Qu'y
   gagne-t-on, qu'y perd-on&nbsp;?
2. Installez le hook git avec `uvx pre-commit install`, puis vérifiez tout le dépôt avec
   `uvx pre-commit run --all-files`.
3. Ajoutez à `options.py` un import inutilisé et une erreur de typage, puis essayez de
   commiter (`git commit -am "Essai"`)&nbsp;: observez le refus, et ce que `ruff` a
   corrigé seul. Ajoutez ensuite, sous l'erreur de typage, la ligne `y: int = "a" #
   pyrefly: ignore[bad-assignment]`&nbsp;: que dit `uv run pyrefly check` de ces deux
   lignes&nbsp;? Retirez-les.
4. Un hook se contourne (`git commit --no-verify`)&nbsp;: quelle commande lanceriez-vous
   en intégration continue pour vérifier quand même chaque *pull request*&nbsp;?

**Documentation utile**

- https://pre-commit.com/#repository-local-hooks

<details>
<summary>Conseils supplémentaires</summary>

Un hook local se déclare sous `repo: local`, sans `rev`&nbsp;: `id` et `name` le
nomment, `entry` est la commande à lancer, à laquelle `pre-commit` ajoute les fichiers à
vérifier, `language: system` lui dit de ne rien installer, et `types: [python]` de ne
passer que les fichiers Python. `pyrefly-check` ne change pas&nbsp;: `pre-commit`
l'installe dans un environnement à lui, au premier lancement, et il vérifie tout le
projet, sans en voir les dépendances (celui-ci n'en a pas). Une erreur de typage
s'obtient par exemple avec `x: int = "a"`. Les fichiers que `ruff` a corrigés pendant le
commit refusé sont modifiés mais pas indexés&nbsp;: `git add` les ajoute.

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

`.pre-commit-config.yaml`&nbsp;:

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

Des hooks locaux, on gagne une seule version de `ruff`, celle de `uv.lock`, pour le
hook, la ligne de commande et l'intégration continue, et plus de `rev` à tenir à jour.
On y perd l'isolation&nbsp;: chaque poste doit avoir `uv` et l'environnement du projet,
et `pre-commit autoupdate` ne les suit plus.

```console
uvx pre-commit install
uvx pre-commit run --all-files
git add --all
git commit -m "Vérifier le code à chaque commit"
```

Après l'ajout d'un import inutilisé et de `x: int = "a"` à `options.py`, `git commit -am
"Essai"` est refusé&nbsp;: `ruff-check` a retiré l'import (le fichier est modifié, à
indexer de nouveau), et `pyrefly` signale l'erreur de typage (`bad-assignment`), qu'il
faut corriger à la main. Avec la ligne ignorée en plus, `uv run pyrefly check` dit `1
error (1 suppressed)`.

En intégration continue, `uvx pre-commit run --all-files` lance les mêmes hooks sur
tout le dépôt, et échoue si l'un d'eux échoue, qu'on ait commité avec `--no-verify` ou
non. Les commandes `uv run ruff check`, `uv run ruff format --check` et `uv run pyrefly
check` conviennent aussi&nbsp;: elles ne corrigent rien, là où le hook lance `--fix`, et
`pyrefly` y tourne à la version de `uv.lock`, avec les dépendances du projet.

</details>

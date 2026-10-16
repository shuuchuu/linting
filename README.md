# Linting

[![Open in GitHub Codespaces](https://github.com/codespaces/badge.svg)](https://codespaces.new/shuuchuu/linting)

## Typage des fonctions et classes

Utilisez l'outil `ty` pour détecter les erreurs de typage du fichier `code_to_type.py` puis corrigez-les.

Vous pouvez lancer les fonctions à typer avec la commande `python -m linting.code_to_type` dans le terminal.

## Détection de défauts

Utilisez l'outil `ruff` pour détecter les défauts présents dans le fichier `options.py` puis corrigez-les.

## Détection de code trop complexe

`ruff` dispose d'un mécanisme de détection de code trop complexe, basé sur la [complexité cyclomatique](https://fr.wikipedia.org/wiki/Nombre_cyclomatique).

Éditez le fichier `pyproject` de configuration pour que l'outil détecte les fonctions trop complexes ([règle C901](https://docs.astral.sh/ruff/rules/#mccabe-c90) & [l'option liée](https://docs.astral.sh/ruff/settings/#lintmccabe)).

Trouvez la valeur maximale qui vous renvoie une erreur puis observez la fonction mentionnée.

Vous pouvez ensuite mettre une valeur de `10` à ce paramètre pour le reste des travaux pratiques.

## Formatage du code

Le formatage du code fait perdre beaucoup de temps en revue de code et pendant l'écriture de code. Une option très intéressante et de déléguer complètement cette tâche à un outil dédié. En Python, `ruff` peut s'en charger.

Dans ces travaux pratiques, `ruff` est déjà configuré pour tourner à chaque sauvegarde. Essayez de modifier le code puis observez le résultat de l'exécution de `ruff` quand vous sauvegardez.

## Qualité de la documentation

La documentation est une partie très importante du code.

Pour lutter contre la dérive de la documentation —l'obsolescence progressive usuelle de la documentation par rapport au code— il est important de s'outiller.

Activez les règles `D` & `DOC` dans la configuration de `ruff` et activez le mode preview (`preview = true`).

Configurez aussi le style de la documentation pour utiliser le style `google`, comme expliqué dans la [documentation](https://docs.astral.sh/ruff/settings/#lintpydocstyle).

Corrigez les défauts que vous pourriez relever.

## Automatisation des vérifications avec `pre-commit`

Plutôt que de compter sur chacun pour lancer les vérifications, faites-les tourner à chaque `git commit` avec [`pre-commit`](https://pre-commit.com/) :

1. Créez à la racine du dépôt un fichier `.pre-commit-config.yaml` qui déclare les hooks `ruff-check` (avec l'argument `--fix`) et `ruff-format` du dépôt [`ruff-pre-commit`](https://github.com/astral-sh/ruff-pre-commit), et le hook `ty` du dépôt [`ty-pre-commit`](https://github.com/astral-sh/ty-pre-commit), aux versions (`rev`) de `ruff` et `ty` que vous utilisez.
2. Installez le hook git avec `uvx pre-commit install`, puis vérifiez tout le dépôt avec `uvx pre-commit run --all-files`.
3. Ajoutez à `options.py` un import inutilisé et une erreur de typage, puis essayez de commiter : observez le refus, et ce que `ruff` a corrigé seul.
4. Un hook se contourne (`git commit --no-verify`) : quelle commande lanceriez-vous en intégration continue pour vérifier quand même chaque PR ?

## Solutions sur GitHub

Vous trouverez ici les solutions proposées : [branche solution de ce dépôt](https://github.com/shuuchuu/linting/tree/solution).

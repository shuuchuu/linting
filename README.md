# Linting

[![Open in GitHub Codespaces](https://github.com/codespaces/badge.svg)](https://codespaces.new/shuuchuu/linting/tree/main-en)

## Function and Class Typing

Use `mypy` to detect type errors in the `code_to_type.py` file and correct them.

You can run the functions that need typing with the following command in the terminal:

```sh
python -m linting.code_to_type
```

## Defect Detection

Use `ruff` to detect defects in the `options.py` file and correct them.

## Detecting Overly Complex Code

`ruff` includes a mechanism to detect overly complex code based on [cyclomatic complexity](https://en.wikipedia.org/wiki/Cyclomatic_complexity).

Edit the `pyproject` configuration file to enable detection of overly complex functions ([Rule C901](https://docs.astral.sh/ruff/rules/#mccabe-c90) & [related option](https://docs.astral.sh/ruff/settings/#lintmccabe)).

Find the maximal value that triggers an error, then examine the mentioned function.

After that, set this parameter to `10` for the rest of the labs.

## Code Formatting

Code formatting can be a time-consuming task during code reviews and development. A great solution is to delegate this entirely to a dedicated tool. In Python, `ruff` can handle this.

In these exercises, `ruff` is already configured to run automatically on every save. Try modifying the code and observe how `ruff` formats it when you save.

## Documentation Quality

Documentation is a crucial part of a codebase.

To prevent documentation from becoming outdated over time, it’s important to use appropriate tools.

Enable `D` & `DOC` rules in `ruff`'s configuration and activate preview mode (`preview = true`).

Fix any documentation issues that arise.

## Creating a Command to Run All Checks

Create a `Makefile` that consolidates all the tools into a single command for easier execution.

## Solutions on GitHub

You can find the proposed solutions here: [solution-en branch of this repository](https://github.com/shuuchuu/linting/tree/solution-en).

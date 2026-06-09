# Linting

[![Open in GitHub Codespaces](https://github.com/codespaces/badge.svg)](https://codespaces.new/shuuchuu/linting/tree/main-en)

## Function and Class Typing

Use the `ty` tool to detect typing errors in the `code_to_type.py` file, then fix them.
You can run the functions to be typed with the command `python -m linting.code_to_type` in the terminal.

## Defect Detection

Use the `ruff` tool to detect defects present in the `options.py` file, then fix them.

## Overly Complex Code Detection

`ruff` has a mechanism for detecting overly complex code, based on [cyclomatic complexity](https://en.wikipedia.org/wiki/Cyclomatic_complexity).
Edit the `pyproject` configuration file so that the tool detects overly complex functions ([rule C901](https://docs.astral.sh/ruff/rules/#mccabe-c90) & [the related option](https://docs.astral.sh/ruff/settings/#lintmccabe)).
Find the maximum value that returns an error, then observe the mentioned function.
You can then set this parameter to a value of `10` for the rest of the practical work.

## Code Formatting

Code formatting wastes a lot of time during code reviews and while writing code. A very interesting option is to delegate this task entirely to a dedicated tool. In Python, `ruff` can handle it.
In this hands-on lab, `ruff` is already configured to run on every save. Try modifying the code, then observe the result of `ruff` executing when you save.

## Documentation Quality

Documentation is a very important part of the code.
To combat documentation drift — the usual progressive obsolescence of documentation relative to the code — it is important to have the right tools.
Enable the `D` & `DOC` rules in the `ruff` configuration and enable preview mode (`preview = true`).
Also configure the documentation style to use the `google` style, as explained in the [documentation](https://docs.astral.sh/ruff/settings/#lintpydocstyle).
Fix any defects you may find.

## Creating a Command That Groups All Checks

Create a `dodo.yml` file to use the [doit](https://pydoit.org/index.html) library and specify a task in it to run all the verification tools.

## Solutions on GitHub

You will find the proposed solutions here: [solution branch of this repository](https://github.com/shuuchuu/linting/tree/solution-en).

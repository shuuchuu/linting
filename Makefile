check:
	ruff check src/linting
	mypy src/linting

.PHONY: check

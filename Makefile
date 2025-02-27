# Variables
PYTHON = uv
SRC_DIR = src
TEST_DIR = tests

.PHONY: help setup format lint test precommit docs clean

## Show all available commands
help:
	@echo "Available commands:"
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-18s\033[0m %s\n", $$1, $$2}'

setup:
	uv venv .venv
	uv sync
	pre-commit install --hook-type pre-commit
	pre-commit install --hook-type pre-push

## Format code using Ruff
format:
	$(PYTHON) run ruff format $(SRC_DIR) $(TEST_DIR)

## Lint code using Ruff
lint:
	$(PYTHON) run ruff check $(SRC_DIR) $(TEST_DIR)

## Run tests using pytest
# check:
# 	$(PYTHON) run pytest $(TEST_DIR)
test:
	echo "No tests to run"


## Run pre-commit hooks
precommit:
	pre-commit run --all-files

## Generate documentation using MkDocs
docs:
	mkdocs serve

## Clean up generated files
clean:
	rm -rf __pycache__ .pytest_cache .mypy_cache .ruff_cache

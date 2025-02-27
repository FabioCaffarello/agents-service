# Variables
version?=latest
PYTHON = uv
PACKAGES_DIR = packages
SRC_DIR = src
TEST_DIR = tests
REGISTRY_NAME = fabiocaffarello
SERVICE_NAME = agents-service
NB_IMAGE_NAME = $(REGISTRY_NAME)/$(SERVICE_NAME)-notebook

.PHONY: help setup coverage format lint check precommit serve-docs deploy-docs clean

## Show all available commands
help:
	@echo "Available commands:"
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-18s\033[0m %s\n", $$1, $$2}'

setup:
	uv venv .venv
	uv sync --all-extras
	chmod +x scripts/branch-check.sh
	pre-commit install --hook-type pre-commit
	pre-commit install --hook-type pre-push

## Format code using Ruff
format:
	$(PYTHON) run ruff format $(SRC_DIR) $(PACKAGES_DIR) $(TEST_DIR)

## Lint code using Ruff
lint:
	$(PYTHON) run ruff check $(SRC_DIR) $(PACKAGES_DIR) $(TEST_DIR)

## Run tests using pytest
check:
	$(PYTHON) run pytest $(PACKAGES_DIR)

## Run tests using pytest with coverage
coverage:
	uv run coverage erase
	$(PYTHON) run pytest --cov=$(PACKAGES_DIR) --cov-report=term-missing --cov-config=.coveragerc

## Run pre-commit hooks
precommit:
	pre-commit run --all-files

## Generate documentation using MkDocs
server-docs:
	$(PYTHON) run -- python -m mkdocs serve

## Deploy documentation to GitHub Pages
deploy-docs:
	$(PYTHON) run -- python -m mkdocs gh-deploy

## Clean up generated files
clean:
	@echo "Cleaning up cache directories and temporary files..."
	# Remove all __pycache__ directories
	find . -type d -name "__pycache__" -exec rm -rf {} +
	# Remove .pytest_cache, .mypy_cache, and .ruff_cache directories
	find . -type d -name ".pytest_cache" -exec rm -rf {} +
	find . -type d -name ".mypy_cache" -exec rm -rf {} +
	find . -type d -name ".ruff_cache" -exec rm -rf {} +
	# Remove all .pyc files
	find . -type f -name "*.pyc" -delete
	@echo "Clean complete."

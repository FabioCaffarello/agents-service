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

lint-docstrings:
	$(PYTHON) run pydoclint --style=google --check-return-types=false --exclude=.venv .

## Run tests using pytest
check:
	$(PYTHON) run pytest $(PACKAGES_DIR)

## Run tests using pytest with coverage and generate a report
coverage-report:
	@echo "Erasing old coverage files (excluding .coveragerc)..."
	find . -maxdepth 1 -type f -name ".coverage*" ! -name ".coveragerc" -exec rm -f {} +
	@echo "Erasing internal coverage data..."
	uv run coverage erase
	@echo "Running tests with coverage..."
	COVERAGE_FILE=.coverage.single $(PYTHON) run pytest --maxfail=1 --disable-warnings --cov=$(PACKAGES_DIR) --cov-report=term-missing --cov-report=html --cov-config=.coveragerc > cov-report.txt
	@echo "Removing generated coverage file..."
	rm -f .coverage.single

## Run tests using pytest with coverage
coverage:
	@echo "Erasing old coverage files (excluding .coveragerc)..."
	find . -maxdepth 1 -type f -name ".coverage*" ! -name ".coveragerc" -exec rm -f {} +
	@echo "Erasing internal coverage data..."
	uv run coverage erase
	@echo "Running tests with coverage..."
	COVERAGE_FILE=.coverage.single $(PYTHON) run pytest --maxfail=1 --disable-warnings --cov=$(PACKAGES_DIR) --cov-report=term-missing --cov-config=.coveragerc
	@echo "Removing generated coverage file..."
	rm -f .coverage.single

## Run pre-commit hooks
precommit:
	pre-commit run --all-files

## Generate documentation using MkDocs
server-docs:
	docker run -d -p 8080:8080 plantuml/plantuml-server:jetty
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

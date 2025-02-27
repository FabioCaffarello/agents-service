# Getting Started with Agents Service


Welcome to **Agents Service** – an agentic microservice built using LangGraph. This guide will help you set up the project on your local machine, run the service, and get started with development.

---

## Prerequisites

Before you begin, ensure you have the following installed:

- **Python 3.12** or higher
- **uv** – a modern dependency and environment manager
  *(Installation instructions: [uv GitHub Repository](https://github.com/astral-sh/uv))*
- **Docker**

---

## 1. Clone the Repository

First, clone the repository from GitHub:

```bash
git clone https://github.com/FabioCaffarello/agents-service.git
cd agents-service
```

---

## 2. Set Up the Virtual Environment

Your project uses **uv** to manage the virtual environment and dependencies. The Makefile includes a `setup` target that handles environment creation, dependency installation, and pre-commit hook setup.

Run the following command to set up the project:

```bash
make setup
```

This command performs the following steps:
- Creates a virtual environment in the `.venv` directory.
- Installs all dependencies including development and documentation extras.
- Sets executable permissions on the branch-check script.
- Installs the pre-commit hooks for both commit and push stages.

---

## 3. Running the Service

To start the development server (with auto-reload), run:

<!-- ```bash
uv run python -m uvicorn src.main:app --reload
```

Then, open your browser and visit [http://127.0.0.1:8000](http://127.0.0.1:8000) to view the service.

--- -->

## 4. Running Tests

To run the test suite, use the Makefile target for checking tests:

```bash
make check
```

This command executes `pytest` within the uv-managed environment.

---

## 5. Linting and Code Quality

To format and lint your code, use the following targets:

- **Format Code (using Ruff):**

  ```bash
  make format
  ```

- **Lint Code (using Ruff):**

  ```bash
  make lint
  ```

- **Run Pre-commit Hooks:**

  ```bash
  make precommit
  ```

---

## 6. Documentation

### Serve Documentation Locally

Your project documentation is managed with MkDocs. To serve the docs locally with live-reloading, run:

```bash
make server-docs
```

Then, visit [http://127.0.0.1:8000](http://127.0.0.1:8000) in your browser.

### Deploy Documentation

To deploy the documentation to GitHub Pages, run:

```bash
make deploy-docs
```

This command will build the documentation and push it to the appropriate branch for GitHub Pages.

---

## 7. Additional Commands

For other tasks, refer to the Makefile by running:

```bash
make help
```

This will list all available commands and their descriptions.

---

## 8. Troubleshooting

- **Virtual Environment Issues:**
  If you encounter any issues with the virtual environment, try running `make clean` to clear caches and temporary files, then run `make setup` again.

- **Pre-commit Hooks:**
  If pre-commit hooks aren’t running as expected, ensure they’re installed by running:

  ```bash
  pre-commit install
  ```

- **Dependency Updates:**
  When you update your dependencies in `pyproject.toml`, remember to run:

  ```bash
  uv lock
  ```

  to update the lock file.

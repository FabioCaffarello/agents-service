# Logger Library

A simple logging library for Agents Service that provides JSON-formatted logging using [python-json-logger](https://github.com/madzak/python-json-logger). This library is designed to integrate seamlessly with your application while enabling structured logging for better observability and easier log parsing.

## Features

- **JSON-Formatted Logging:** Outputs log messages in JSON format, making it easier to ingest logs in modern logging systems.
- **Configurable Log Levels:** Set the log level via environment variables or directly in your code.
- **Easy Integration:** Simple API to set up logging in any module.

## Usage

Here's a quick example of how to use the logger library in your code:

```python
from logger.log import setup_logging

# Set up the logger for the current module
logger = setup_logging(__name__, log_level="DEBUG")

logger.info("This is an informational message.")
logger.error("An error occurred!", extra={"error_code": 123})
```

## Testing

To run the tests for this library, navigate to the logger project directory and run:

```bash
uv --project packages/logger run pytest --cov=packages/logger/src/logger --cov-report=term-missing --cov-config=.coveragerc
```

This will execute the tests defined in the `packages/logger/tests` directory with coverage.

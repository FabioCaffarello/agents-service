# Config

The **Config** module provides a centralized configuration class for the agents-service. Using Python’s dataclasses, this module simplifies handling configuration values that can be populated from environment variables and command-line arguments.

## Features

- **Default Settings:**
  The `Config` class sets sensible defaults (for example, a log level of `INFO`) and reads environment variables to override those defaults.

- **Validation:**
  The configuration is validated upon instantiation, ensuring that only supported log levels (e.g., DEBUG, INFO, WARNING, ERROR, CRITICAL) are accepted.

- **Simplicity and Extensibility:**
  Easily extend the `Config` dataclass with additional fields for more configuration options as your service grows.

## Usage

Import and create an instance of `Config` to access your configuration settings:

```python
from config.core import Config

# Create a configuration instance; environment variables (e.g., LOG_LEVEL) will override defaults
config = Config()

print(f"Log Level: {config.log_level}")
print(f"Verbose: {config.verbose}")
print(f"Debug: {config.debug}")
```

## Example

Below is an example of how the configuration might be loaded from command-line arguments and environment variables in your main service:

```python
import os
from cliargs.cli import new_args_parser
from config.core import Config

def load_config_from_args(args) -> Config:
    return Config(
        log_level=args.log_level,
        verbose=args.verbose,
        debug=args.debug,
    )

parser = new_args_parser("Run agents-service.")
parser.add_argument("--agent", type=str, help="Name of the agent to run")
parser.add_argument("--config", type=str, default="config.yaml", help="Path to configuration file")
args = parser.parse_args()

config = load_config_from_args(args)
print(config)
```

## Testing

To run the tests for this library, navigate to the logger project directory and run:

```bash
uv --project packages/config run pytest --cov=packages/config/src/config --cov-report=term-missing --cov-config=.coveragerc
```

This will execute the tests defined in the `packages/config/tests` directory with coverage.

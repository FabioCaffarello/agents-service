# CLIargs

**CLIargs** is a lightweight command-line interface helper library for Python, built on top of the standard `argparse` module. It provides a simple, consistent way to create and configure argument parsers with common utility flags that can be used across your applications.

## Features

- **Easy Parser Creation:** Quickly create an `ArgumentParser` with a provided description.
- **Common Utility Flags:** Pre-configured flags for verbosity, debugging, logging levels, and version information.
- **Extensible:** Built as a foundation that you can easily extend with custom flags and subcommands.

## Usage

Here's a basic example demonstrating how to create and use an argument parser with CLIargs:

```python
from cliargs.cli import new_args_parser

def main():
    parser = new_args_parser("Example Application")
    args = parser.parse_args()

    if args.verbose:
        print("Verbose mode enabled.")
    if args.debug:
        print("Debug mode is active.")

    print(f"Log level: {args.log_level}")
    print(f"Configuration file: {args.config}")

if __name__ == '__main__':
    main()
```

### Available Flags

- **`--verbose`**: Enable verbose output.
- **`--debug`**: Activate debug mode with detailed logging.
- **`--log-level`**: Set the logging level (choices: DEBUG, INFO, WARNING, ERROR, CRITICAL; defaults to INFO).
- **`--version`**: Print the library’s version and exit.

## Testing

To run the tests for this library, navigate to the logger project directory and run:

```bash
uv --project packages/cliargs run pytest --cov=packages/cliargs/src/cliargs --cov-report=term-missing --cov-config=.coveragerc
```

This will execute the tests defined in the `packages/cliargs/tests` directory with coverage.

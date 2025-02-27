# %%
import logging
from logger.log import setup_logging
from cliargs.cli import new_args_parser
from config.core import Config


def load_config_from_args(args) -> Config:
    """
    Create a Config instance from command-line arguments.
    """
    return Config(
        log_level=args.log_level,
        verbose=args.verbose,
        debug=args.debug,
    )


def setup_service() -> tuple[Config, logging.Logger]:
    """
    Parse CLI arguments, load the configuration, and set up logging.
    Returns a tuple of (Config, Logger).
    """
    parser = new_args_parser("Run agents-service.")
    args = parser.parse_args()
    config = load_config_from_args(args)

    log = setup_logging(__file__, log_level=args.log_level)
    if args.verbose:
        log.info("Verbose mode enabled.")
    if args.debug:
        log.info("Debug mode activated.")
    return config, log


def main():
    config, log = setup_service()
    log.info(f"Loaded configuration: {config}")


if __name__ == "__main__":
    main()

# %%

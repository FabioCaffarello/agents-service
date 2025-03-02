import asyncio
import logging
import multiprocessing
import sys
import uvicorn
from server.signal_handler import SignalHandler
from cliargs.cli import new_args_parser
from config.core import Config
from logger.log import setup_logging
from presenters.rest.api import app as rest_app
from presenters.websockets.api import app as ws_app


def run_rest_server():
    """Run the REST API server on port 8000."""
    uvicorn.run(rest_app, host="0.0.0.0", port=8000, log_level="info")


def run_ws_server():
    """Run the WebSocket server on port 8001."""
    uvicorn.run(ws_app, host="0.0.0.0", port=8001, log_level="info")


def _set_log_level_env_var(log_level: str):
    """
    Set the `LOG_LEVEL` environment variable for the `logger` module.
    """
    import os

    os.environ["LOG_LEVEL"] = log_level


def setup_service() -> tuple[Config, logging.Logger]:
    """
    Parse CLI arguments, load configuration, and set up logging.
    """
    parser = new_args_parser("Run agents-service.")
    args = parser.parse_args()
    config = Config(
        log_level=args.log_level,
        verbose=args.verbose,
        debug=args.debug,
    )

    log = setup_logging(__file__, log_level=args.log_level)
    _set_log_level_env_var(config.log_level)
    if args.verbose:
        log.info("Verbose mode enabled.")
    if args.debug:
        log.info("Debug mode activated.")

    return config, log


def main():
    config, log = setup_service()
    log.info(f"Loaded configuration: {config}")

    rest_process = multiprocessing.Process(target=run_rest_server)
    ws_process = multiprocessing.Process(target=run_ws_server)

    rest_process.start()
    ws_process.start()

    signal_handler = SignalHandler(rest_process, ws_process)

    async def run_signal_handler():
        signal_handler.register_signal_handler()
        # Wait for the shutdown event to be set
        await signal_handler.shutdown.wait()

    try:
        asyncio.run(run_signal_handler())
    except KeyboardInterrupt:
        pass

    rest_process.join()
    ws_process.join()
    # Exit the main function gracefully
    return 0


if __name__ == "__main__":
    sys.exit(main())

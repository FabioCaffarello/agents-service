import asyncio
import signal
import logging

logger = logging.getLogger("shutdown")


class SignalHandler:
    def __init__(self, rest_process, ws_process):
        self.rest_process = rest_process
        self.ws_process = ws_process
        self.shutdown = asyncio.Event()

    async def handle_exit(self, signum, frame):
        logger.info(f"Received termination signal ({signum}), initiating shutdown...")
        self.shutdown.set()

        if self.rest_process and self.rest_process.is_alive():
            logger.info("Stopping REST API server...")
            self.rest_process.terminate()
            self.rest_process.join()

        if self.ws_process and self.ws_process.is_alive():
            logger.info("Stopping WebSocket server...")
            self.ws_process.terminate()
            self.ws_process.join()

        logger.info("All services stopped. Exiting gracefully.")

    def register_signal_handler(self):
        loop = asyncio.get_running_loop()
        for sig in (signal.SIGINT, signal.SIGTERM):
            loop.add_signal_handler(
                sig, lambda s=sig: asyncio.create_task(self.handle_exit(s, None))
            )

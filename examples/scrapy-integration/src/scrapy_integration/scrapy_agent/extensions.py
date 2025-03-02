import json
import asyncio
import websockets
import logging

from scrapy import signals
from twisted.internet import reactor

logger = logging.getLogger(__name__)


class ErrorReportingExtension:
    @classmethod
    def from_crawler(cls, crawler):
        ext = cls()
        crawler.signals.connect(ext.spider_closed, signal=signals.spider_closed)
        crawler.signals.connect(ext.spider_error, signal=signals.spider_error)
        return ext

    def spider_error(self, failure, response, spider):
        # Get the error message.
        error_message = (
            f"Spider '{spider.name}' encountered an error: {failure.getErrorMessage()}"
        )
        # Retrieve the full traceback.
        traceback = failure.getTraceback()
        full_message = f"{error_message}\nTraceback:\n{traceback}"
        self.send_error(full_message, spider)

    def spider_closed(self, spider, reason):
        if reason != "finished":
            error_message = f"Spider '{spider.name}' closed due to error: {reason}"
            self.send_error(error_message, spider)

    def send_error(self, error_message, spider):
        # Log the error message locally.
        spider.logger.error("ErrorReportingExtension: %s", error_message)
        # Build the payload to send.
        payload = {
            "bot_name": spider.name,
            "error": error_message,
            "usage_context": "scraping-error",
        }
        # Schedule the asynchronous sending inside the reactor's event loop.
        reactor.callLater(
            0, lambda: asyncio.create_task(self.send_error_to_ws(payload, spider))
        )

    async def send_error_to_ws(self, payload, spider):
        # Define your websocket endpoint.
        uri = f"ws://localhost:8001/ws/scrapy/{spider.name}/errors"
        spider.logger.info("Connecting to error reporting service at %s", uri)
        try:
            async with websockets.connect(uri) as websocket:
                # Send the payload as JSON.
                await websocket.send(json.dumps(payload))
                spider.logger.info("Sent error payload: %s", payload)
                # Optionally, wait for a response from the server.
                report = await websocket.recv()
                spider.logger.info("Received report: %s", report)
        except Exception as e:
            spider.logger.error("Error sending error payload via WebSocket: %s", e)

import base64
import json
import asyncio
import websockets
import logging

from scrapy import signals
from twisted.internet import reactor


logger = logging.getLogger(__name__)


def safe_decode(value):
    """Safely decode a header value, whether it's bytes, a list of bytes, or already a string."""
    if isinstance(value, bytes):
        return value.decode("utf-8", errors="replace")
    elif isinstance(value, list):
        return [
            x.decode("utf-8", errors="replace") if isinstance(x, bytes) else x
            for x in value
        ]
    else:
        return value


def get_body_snippet(body, length=500, encode_base64=False):
    """Return a snippet of the body limited to 'length' bytes, optionally Base64 encoded."""
    if body:
        if isinstance(body, bytes):
            snippet = body[:length]
        else:
            snippet = body.encode("utf-8")[:length]
        if encode_base64:
            snippet = base64.b64encode(snippet).decode("utf-8")
        else:
            snippet = snippet.decode("utf-8", errors="replace")
        return snippet
    return None


class ReportingMiddleware:
    @classmethod
    def from_crawler(cls, crawler):
        s = cls()
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        return s

    def spider_opened(self, spider):
        logger.info("ReportingMiddleware initialized for spider: %s", spider.name)

    def process_response(self, request, response, spider):
        """
        Process the response, collect metadata, and send it to the reporting service.
        """
        metadata = {
            "usage_context": "scraping",
            "request": {
                "url": request.url,
                "headers": {
                    k.decode("utf-8", errors="replace")
                    if isinstance(k, bytes)
                    else k: safe_decode(v)
                    for k, v in request.headers.items()
                },
                "method": request.method,
            },
            "response": {
                "url": response.url,
                "status": response.status,
                "body": get_body_snippet(response.body, encode_base64=True),
                "headers": {
                    k.decode("utf-8", errors="replace")
                    if isinstance(k, bytes)
                    else k: safe_decode(v)
                    for k, v in response.headers.items()
                },
            },
            "bot_name": spider.name,
        }

        logger.debug("Collected metadata: %s", metadata)
        # Schedule the asynchronous sending inside a proper task context:
        reactor.callLater(
            0, lambda: asyncio.create_task(self.send_metadata(metadata, spider))
        )
        return response

    async def send_metadata(self, metadata, spider):
        """
        Connects to the reporting service WebSocket and sends the metadata.
        """
        uri = f"ws://localhost:8001/ws/scrapy/{spider.name}"
        logger.info("Connecting to reporting service at %s", uri)
        try:
            async with websockets.connect(uri) as websocket:
                await websocket.send(json.dumps(metadata))
                logger.info("Sent metadata: %s", metadata)
                report = await websocket.recv()
                logger.info("Received report: %s", report)
        except Exception as e:
            logger.error("Error sending metadata via WebSocket: %s", e)

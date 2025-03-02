import asyncio
import aiohttp
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
        error_message = (
            f"Spider '{spider.name}' encountered an error: {failure.getErrorMessage()}"
        )
        traceback = failure.getTraceback()
        full_message = f"{error_message}\nTraceback:\n{traceback}"
        self.send_error(full_message, spider)

    def spider_closed(self, spider, reason):
        if reason != "finished":
            error_message = f"Spider '{spider.name}' closed due to error: {reason}"
            self.send_error(error_message, spider)

    def send_error(self, error_message, spider):
        spider.logger.error("ErrorReportingExtension: %s", error_message)
        payload = {
            "bot_name": spider.name,
            "error": error_message,
            "usage_context": "scraping-error",
        }
        reactor.callLater(
            0, lambda: asyncio.create_task(self.send_error_to_ws(payload, spider))
        )

    async def get_access_token(self):
        login_url = "http://127.0.0.1:8000/auth/login"
        credentials = {"username": "admin", "password": "admin123"}
        async with aiohttp.ClientSession() as session:
            async with session.post(login_url, json=credentials) as response:
                if response.status != 200:
                    raise Exception(f"Failed to authenticate: {response.status}")
                data = await response.json()
                return data["access_token"]

    async def send_error_to_ws(self, payload, spider):
        uri = f"ws://localhost:8001/ws/scrapy/{spider.name}/errors"
        spider.logger.info("Connecting to error reporting service at %s", uri)
        try:
            token = await self.get_access_token()
            headers = {"Authorization": f"Bearer {token}"}

            async with aiohttp.ClientSession() as session:
                async with session.ws_connect(uri, headers=headers) as ws:
                    await ws.send_json(payload)
                    spider.logger.info("Sent error payload: %s", payload)
                    # Optionally, wait for a response.
                    async for msg in ws:
                        if msg.type == aiohttp.WSMsgType.TEXT:
                            spider.logger.info("Received report: %s", msg.data)
                            break
                        elif msg.type == aiohttp.WSMsgType.ERROR:
                            break
        except Exception as e:
            spider.logger.error("Error sending error payload via WebSocket: %s", e)

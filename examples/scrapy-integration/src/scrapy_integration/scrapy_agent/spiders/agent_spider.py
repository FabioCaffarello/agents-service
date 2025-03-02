import scrapy


class AgentSpiderSpider(scrapy.Spider):
    name = "agent-spider"
    start_urls = ["https://www.google.com"]

    def start_requests(self):
        for url in self.start_urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        raise Exception("Simulated error for testing error reporting extension")

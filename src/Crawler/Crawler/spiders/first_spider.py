import scrapy
from ..items import CrawlerItem


class FirstSpiderSpider(scrapy.Spider):
    name = "first_spider"
    allowed_domains = ["wikipedia.org"]
    start_urls = ["https://en.wikipedia.org/wiki/United_States"]

    DEPTH_LIMIT = 3

    def parse(self, response):
        # Extracting URLs and titles
        urls = response.css('a::attr(href)').getall()
        title = response.css('title::text').get()

        # Yielding items
        for url in urls:
            if url.startswith('/wiki/') and ':' not in url:
                item = CrawlerItem()
                item['url'] = response.urljoin(url)
                yield item
                yield response.follow(url, callback=self.parse)

        # You can also directly yield a dictionary
        yield {
            'title': title,
            'url': response.url,
        }

    
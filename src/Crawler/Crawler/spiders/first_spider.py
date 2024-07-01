import scrapy
from ..items import CrawlerItem


class FirstSpiderSpider(scrapy.Spider):
    name = "first_spider"
    allowed_domains = ["wikipedia.org"]
    start_urls = ["https://en.wikipedia.org/wiki/United_States"]
    DEPTH_LIMIT = 1

    def parse(self, response):
        # Extracting URLs and titles
        urls = response.css('a::attr(href)').getall()
        title = response.xpath('//title/text()').get()

        main_item = CrawlerItem()
        main_item['url'] = response.url
        main_item['title'] = title
        yield main_item


        # Yielding items
        for url in urls:
            if url.startswith('/wiki/') and ':' not in url:
                yield response.follow(url, callback=self.parse)

    
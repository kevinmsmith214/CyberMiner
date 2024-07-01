# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class CrawlerItem(scrapy.Item):
    url = scrapy.Field()
    title = scrapy.Field()
    keywords = scrapy.Field()
    pass

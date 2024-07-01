# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
import json


class CrawlerPipeline:

    def open_spider(self, spider):
        self.file = open('Output/scraped_data.json', 'a')  # Open file in append mode
        self.file.write("[\n")  # Start with an opening bracket for JSON array

    def process_item(self, item, spider):
        line = json.dumps(dict(item)) + "\n"
        self.file.write(line)
        return item
    
    def close_spider(self, spider):
        self.file.write("]\n")
        self.file.close()
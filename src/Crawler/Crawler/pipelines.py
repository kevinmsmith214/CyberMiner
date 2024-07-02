# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
import json
import os


class CrawlerPipeline:

    def open_spider(self, spider):
        self.file_path = 'Output/scraped_data.json'
        if os.path.exists(self.file_path):
            os.remove(self.file_path)  # Remove the file if it exists
        self.file = open(self.file_path, 'a')
    def process_item(self, item, spider):
        line = json.dumps(dict(item)) + ",\n"
        self.file.write(line)
        return item
    
    def close_spider(self, spider):
        self.file.close()
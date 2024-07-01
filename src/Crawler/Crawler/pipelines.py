# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
import boto3
from scrapy.exceptions import DropItem
from scrapy import log


class CrawlerPipeline:
    def __init__(self, aws_access_key_id, aws_secret_access_key, aws_region_name, table_name):
        self.aws_access_key_id = aws_access_key_id
        self.aws_secret_access_key = aws_secret_access_key
        self.aws_region_name = aws_region_name
        self.table_name = table_name

    @classmethod
    def from_crawler(cls, crawler):
        return cls(
            aws_access_key_id=crawler.settings.get('AWS_ACCESS_KEY_ID'),
            aws_secret_access_key=crawler.settings.get('AWS_SECRET_ACCESS_KEY'),
            aws_region_name=crawler.settings.get('AWS_REGION_NAME'),
            table_name=crawler.settings.get('DYNAMODB_TABLE_NAME')
        ) 
  
    def open_spider(self, spider):
        self.dynamodb = boto3.resource('dynamodb',
            aws_access_key_id=self.aws_access_key_id,
            aws_secret_access_key=self.aws_secret_access_key,
            region_name=self.aws_region_name
        )
        self.table = self.dynamodb.Table(self.table_name)

    def close_spider(self, spider):
        pass

    def process_item(self, item, spider):
        data = {
            'url': item['url'],
            'title': item.get('title', ''),
        }

        try:
            self.table.put_item(Item=data)
            log.msg(f"Item stored in DynamoDB: {data}", level=log.INFO)
        except Exception as e:
            log.msg(f"Failed to store item in DynamoDB: {e}", level=log.ERROR)
            raise DropItem(f"Failed to store item in DynamoDB: {e}")

        return item
# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
import json

from scrapy import log
import pymongo
from scrapy.exceptions import DropItem


class HupuScrapyPipeline(object):
    def process_item(self, item, spider):
        return item

class BXJItemPipeline(object):

    def __init__(self):
        log.start(logfile=None, loglevel=log.DEBUG, logstdout=True)


    def process_item(self, item, spider):
        if item['title_page_url']:
            return item
        else:
            raise DropItem("Miss price in %s" % item)

    def open_spider(self, spider):
        log.msg("Hello!\r\n")

    def close_spider(self, spider):
        log.msg("Hello!\r\n")

class BXJItemJsonWirterPipeline(object):

    def __init__(self):
        self.file = open('BXJItem.jl', 'wb')

    def process_item(self, item, spider):
        line = json.dumps(dict(item)) + "\n"
        self.file.write(line)
        return item

class BXJItemMongoPipeline(object):

    def __init__(self, mongo_uri, mongo_db):
        self.mongo_uri = mongo_uri
        self.mongo_db = mongo_db

    @classmethod
    def from_crawler(cls, crawler):
        return cls(
            mongo_uri=crawler.settings.get('MONGO_URI'),
            mongo_db=crawler.settings.get('MONGO_DATABASE', 'hupu')
        )

    def open_spider(self, spider):
        self.client = pymongo.MongoClient(self.mongo_uri)
        self.db = self.client[self.mongo_db]

    def close_spider(self, spider):
        self.client.close()

    def process_item(self, item, spider):
        collection_name = item.__class__.__name__
        print collection_name
        self.db[collection_name].insert(dict(item))
        return item


# class BXJItemDuplicatesPipeline(object):
#
#     def __init__(self):
#         self.ids_seen = set()
#
#     def process_item(self, item, spider):
#         if item['title_page_url'] in self.ids_seen:
#             raise DropItem("Duplicate item found: %s" % item)
#         else:
#             self.ids_seen.add(item['id'])
#             return item
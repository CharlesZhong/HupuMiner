# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
import json

from scrapy import log
import pymongo
from scrapy.exceptions import DropItem
import re
from datetime import datetime,timedelta
class HupuScrapyPipeline(object):
    def process_item(self, item, spider):
        return item

class BXJItemPipeline(object):

    re_light_reply = re.compile(ur'有(\d)个亮了的回帖')
    re_reply_browse = re.compile(ur'(\d*)\s*/\s*(\d*)')
    def __init__(self):
        log.start(logfile=None, loglevel=log.DEBUG, logstdout=True)

    def process_item(self, item, spider):

        item["create_date"] = unicode(item["create_date"][0]) if item["create_date"] else ""


        create_date = datetime.strptime(item["create_date"],"%Y-%m-%d")



        delta = datetime.today() - create_date

        if not item['create_date'] or item['create_date'] == u"":
            raise DropItem("Miss create_time in %s" % item)
        elif not item['title_page_url'] or item['title_page_url'] == u"":
            raise DropItem("Miss title_page_url in %s" % item)

        elif delta.days != 1:
            raise DropItem("Not Yesterday's data %s" % item)
        else :
            for key in ["username", "username_url",
                        "title", "title_page_url",  "zone", "zone_prefix",
                        "light_replay","reply_browse",
                        "last_reply_time","last_reply_url","last_reply_username",]:
                item[key] = unicode(item[key][0]) if item[key] else ""

            if item["light_replay"]:
                match = self.re_light_reply.match(item["light_replay"])
                item["light_replay"] = int(match.groups()[0]) if match else 0
            else:
                item["light_replay"] = 0

            if item["reply_browse"]:
                match = self.re_reply_browse.match(item["reply_browse"])
                item["reply_count"], item["browse_count"] = map(lambda x:int(x),match.groups()) if match else (0,0)

            if not item["zone"]: item["zone"] = u"bxj"
            if not item["zone_prefix"]: item["zone"] = u"/bxj"

            return item






    def open_spider(self, spider):
        log.msg("Hello")

    def close_spider(self, spider):
        log.msg("Bye")





class BXJItemDuplicatesPipeline(object):

    def __init__(self):
        self.ids_seen = set()

    def process_item(self, item, spider):
        if item['title_page_url'] in self.ids_seen:
            raise DropItem("Duplicate item found: %s" % item)
        else:
            self.ids_seen.add(item['title_page_url'])
            return item


class BXJItemJsonWirterPipeline(object):

    def __init__(self):
        self.file = open('BXJItem.json', 'wb')

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



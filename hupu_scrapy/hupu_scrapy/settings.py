# -*- coding: utf-8 -*-

# Scrapy settings for hupu_scrapy project
#
# For simplicity, this file contains only the most important settings by
# default. All the other settings are documented here:
#
#     http://doc.scrapy.org/en/latest/topics/settings.html
#
import os
BOT_NAME = 'hupu_scrapy'

SPIDER_MODULES = ['hupu_scrapy.spiders']
NEWSPIDER_MODULE = 'hupu_scrapy.spiders'

# Crawl responsibly by identifying yourself (and your website) on the user-agent
#USER_AGENT = 'hupu_scrapy (+http://www.yourdomain.com)'


MONGO_USER = os.environ.get('MONGO_USER')
MONGO_PASSWORD = os.environ.get('MONGO_PASSWORD')
MONGO_URI= 'mongodb://127.0.0.1:27017'
MONGO_DATABASE = 'hupu'


ITEM_PIPELINES = {
    BOT_NAME+'.pipelines.BXJItemPipeline': 300,
    BOT_NAME+'.pipelines.BXJItemDuplicatesPipeline': 301,
    BOT_NAME+'.pipelines.BXJItemJsonWirterPipeline': 302,
    BOT_NAME+'.pipelines.BXJItemMongoPipeline': 303,
}
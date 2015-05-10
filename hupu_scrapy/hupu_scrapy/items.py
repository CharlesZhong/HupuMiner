# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class BxjItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
	title_page_url = scrapy.Field()
	title_mulitpage_urls = scrapy.Field()
	title = scrapy.Field()

	username_url = scrapy.Field()
	username = scrapy.Field()

	zone = scrapy.Field()
	zone_prefix = scrapy.Field()

	reply_count = scrapy.Field()
	browse_count = scrapy.Field()
	light_replay = scrapy.Field()

	create_date = scrapy.Field()

	last_reply_username = scrapy.Field()
	last_reply_time = scrapy.Field()
	last_reply_url = scrapy.Field()

	

    

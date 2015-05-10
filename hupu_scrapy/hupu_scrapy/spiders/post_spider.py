# -*- coding: UTF-8 -*-
import scrapy
class PostSpider(scrapy.Spider):
	name = "post"
	allowed_domains = ["hupu.com"]
	start_urls = [
		"http://bbs.hupu.com/bxj",
		]


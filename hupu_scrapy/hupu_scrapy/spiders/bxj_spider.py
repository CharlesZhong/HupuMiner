# -*- coding: UTF-8 -*-
import scrapy

from hupu_scrapy.items import BXJItem


class BXJSpider(scrapy.Spider):
    name = "bxj"
    allowed_domains = ["bbs.hupu.com"]
    start_urls = [ "http://bbs.hupu.com/bxj-postdate-"+str(idx) for idx in xrange(1, 100)]

    def parse(self, response):

        self.log("[BXJ Spider]", level=scrapy.log.INFO)

        table = response.xpath('//table[@id="pl"]')
        for tr in table.xpath('.//tr'):
            
            node_title = tr.xpath('./td[@class="p_title"]')
            if node_title:
                item = BXJItem()
                item['title'] = node_title.xpath('./a[@id]/text()').extract()
                
                item['zone'] = node_title.xpath('./a[not(@id)]/text()').extract()
                item['zone_prefix'] = node_title.xpath('./a[not(@id)]/@href').extract()
                item['title_page_url'] = node_title.xpath('./a[@id]/@href').extract()
                item['title_mulitpage_urls'] = node_title.xpath('./span[@class="multipage"]/a/@href').extract()
                item['light_replay'] = node_title.xpath('./child::span/a/@title').extract()
                


                node_author = tr.xpath('./td[@class="p_author"]')
                if node_author:
                    item['username'] = node_author.xpath('./a/text()').extract()
                    item['username_url'] = node_author.xpath('./a/@href').extract()
                    item['create_date'] = node_author.xpath('./text()').extract()

                node_re = tr.xpath('./td[@class="p_re"]')
                if node_re:
                    reply_browse = node_re.xpath('./text()').extract()

                    item['reply_count'],item['browse_count'] = map(lambda x: x.strip(),reply_browse[0].split("/")) if reply_browse else (None,None)
                node_retime = tr.xpath('./td[@class="p_retime"]')
                if node_retime:
                    item['last_reply_time']= node_retime.xpath('./a/text()').extract()
                    item['last_reply_url']= node_retime.xpath('./a/@href').extract()
                    item['last_reply_username']= node_retime.xpath('./text()').extract()

                yield item


                
    def change_item(self, item):

        if item and isinstance(item, dict):



            return "\r\n".join([k+":"+reduce(lambda x,y: x + "|" + y ,map(lambda x: x.encode('utf8'), v)) if v else k+":None" for k, v in item.iteritems()])+"\r\n\r\n"


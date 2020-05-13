# -*- coding: utf-8 -*-
import scrapy
import json
from scrapy import Request, Spider
from zhihu_scrapy.items import UserItem
import time

class ZhihuArticleSpider(scrapy.Spider):
    name = 'article'
    allowed_domains = ['www.zhihu.com']
    start_urls = ['http://www.zhihu.com/']
    start_urls = ['http://zhihu.com/']
    def start_requests(self):
        yield Request('https://www.zhihu.com/api/v4/search_v3?t=general&q=23&correction=1&offset=0&limit=20&lc_idx=0&show_all_topics=0', callback=self.parse_page)
        # yield Request(self.follows_url.format(user=self.start_user, include=self.follows_query, offset=0, limit=20),
        #               callback = self.parse_page)
    def parse_page(self, response):
        result = response.text
        print(result)

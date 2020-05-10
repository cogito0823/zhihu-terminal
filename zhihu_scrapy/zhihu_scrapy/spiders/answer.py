# -*- coding: utf-8 -*-
import scrapy


class ZhihuAnswerSpider(scrapy.Spider):
    name = 'zhihu_answer'
    allowed_domains = ['zhihu.com']
    start_urls = ['http://zhihu.com/']

    def parse(self, response):
        pass

# -*- coding: utf-8 -*-
import scrapy


class ZhihuArticleSpider(scrapy.Spider):
    name = 'zhihu_article'
    allowed_domains = ['zhihu.com']
    start_urls = ['http://zhihu.com/']

    def parse(self, response):
        pass

#! /usr/bin/env python3
# -*- coding: utf-8 -*-
from twisted.internet import reactor
from scrapy.crawler import CrawlerRunner
from scrapy.utils.project import get_project_settings
from scrapy.utils.log import configure_logging
# 引入spider
from zhihu_scrapy.spiders.user import UserSpider
import logging


logger = logging.getLogger(__name__)

settings = get_project_settings()
configure_logging(settings)
runner = CrawlerRunner(settings)


def start_spider():
    # 装载爬虫
    runner.crawl(UserSpider)
    # 如果有多个爬虫需要启动可以一直装载下去
    # runner.crawl(TestSpider2)
    # runner.crawl(TestSpider3)
    # runner.crawl(TestSpider4)
    # ... ...
    
    # 爬虫结束后停止事件循环
    d = runner.join()
    d.addBoth(lambda _: reactor.stop())

    # 启动事件循环
    reactor.run()


def main():
    start_spider()


if __name__ == '__main__':
    main()

# -*- coding: utf-8 -*-

# Define here the models for your spider middleware
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/spider-middleware.html

from scrapy import signals
import hashlib
import time
import sys

class ZhihuuserSpiderMiddleware(object):
    # Not all methods need to be defined. If a method is not defined,
    # scrapy acts as if the spider middleware does not modify the
    # passed objects.

    @classmethod
    def from_crawler(cls, crawler):
        # This method is used by Scrapy to create your spiders.
        s = cls()
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        return s

    def process_spider_input(self, response, spider):
        # Called for each response that goes through the spider
        # middleware and into the spider.

        # Should return None or raise an exception.
        return None

    def process_spider_output(self, response, result, spider):
        # Called with the results returned from the Spider, after
        # it has processed the response.

        # Must return an iterable of Request, dict or Item objects.
        for i in result:
            yield i

    def process_spider_exception(self, response, exception, spider):
        # Called when a spider or process_spider_input() method
        # (from other spider middleware) raises an exception.

        # Should return either None or an iterable of Response, dict
        # or Item objects.
        pass

    def process_start_requests(self, start_requests, spider):
        # Called with the start requests of the spider, and works
        # similarly to the process_spider_output() method, except
        # that it doesn’t have a response associated.

        # Must return only requests (not items).
        for r in start_requests:
            yield r

    def spider_opened(self, spider):
        spider.logger.info('Spider opened: %s' % spider.name)


class ZhihuuserDownloaderMiddleware(object):
    # Not all methods need to be defined. If a method is not defined,
    # scrapy acts as if the downloader middleware does not modify the
    # passed objects.

    @classmethod
    def from_crawler(cls, crawler):
        # This method is used by Scrapy to create your spiders.
        s = cls()
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        return s

    def process_request(self, request, spider):
        # Called for each request that goes through the downloader
        # middleware.

        # Must either:
        # - return None: continue processing this request
        # - or return a Response object
        # - or return a Request object
        # - or raise IgnoreRequest: process_exception() methods of
        #   installed downloader middleware will be called
        return None

    def process_response(self, request, response, spider):
        # Called with the response returned from the downloader.

        # Must either;
        # - return a Response object
        # - return a Request object
        # - or raise IgnoreRequest
        return response

    def process_exception(self, request, exception, spider):
        # Called when a download handler or a process_request()
        # (from other downloader middleware) raises an exception.

        # Must either:
        # - return None: continue processing this exception
        # - return a Response object: stops process_exception() chain
        # - return a Request object: stops process_exception() chain
        pass

    def spider_opened(self, spider):
        spider.logger.info('Spider opened: %s' % spider.name)


class ProxyMiddleware(object):
    def process_request(self, request, spider):
    #     request.meta['proxy'] = 'http://forward.xdaili.cn:80'
    #     auth = self.tt()
    #     request.headers['Proxy-Authorization'] = auth
        request.meta['proxy'] = 'http://secondtransfer.moguproxy.com:9001'
        request.headers['Proxy-Authorization'] = 'Basic ZnZiajc3Q01zNU1WM1lRMTpBdWFSSDRPYnF6TmRKM1ZF'
        
    # def tt(self):
    #     _version = sys.version_info
    #     is_python3 = (_version[0] == 3)
    #     orderno = "ZF202042702563OjFMf"
    #     secret = "8124740b580246499a8516f75d38186f"
    #     timestamp = str(int(time.time()))              
    #     string = ""
    #     string = "orderno=" + orderno + "," + "secret=" + secret + "," + "timestamp=" + timestamp
    #     if is_python3:                          
    #         string = string.encode()
    #     md5_string = hashlib.md5(string).hexdigest()                
    #     sign = md5_string.upper()
    #     auth = "sign=" + sign + "&" + "orderno=" + orderno + "&" + "timestamp=" + timestamp
    #     return auth       
    def process_exception(self, request, exception, spider):
        # 出现异常时（超时）使用代理
        # print("\n出现异常，正在使用代理重试....\n")
        # request.meta['proxy'] = 'http://forward.xdaili.cn:80'
        # auth = self.tt()
        # request.headers['Proxy-Authorization'] = auth
        # return request
    
        request.meta['proxy'] = 'http://secondtransfer.moguproxy.com:9001'
        request.headers['Proxy-Authorization'] = 'Basic ZnZiajc3Q01zNU1WM1lRMTpBdWFSSDRPYnF6TmRKM1ZF'
        return request
        
    # def process_request(self, request, spider):
    #     request.meta['proxy'] = 'http://117.43.92.46:8889'





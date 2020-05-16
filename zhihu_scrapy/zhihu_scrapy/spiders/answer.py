# -*- coding: utf-8 -*-
import scrapy
import json
from scrapy import Request, Spider
from zhihu_scrapy.items import UserItem
import time

class ZhihuAnswerSpider(scrapy.Spider):
    name = 'zhihu_answer'
    allowed_domains = ['zhihu.com']
    start_urls = ['http://zhihu.com/']
    custom_settings = {
        'MONGO_URI': 'mongodb://answer:asd8561735698@localhost:27017/answer',
        'MONGO_DATABASE': 'answer'
    }
    aswer_url = 'https://www.zhihu.com/api/v4/favlists/{fid}/items?include={include}'
    start_fid = '114929484'
    answer_query = 'data[*].created,content.comment_count,suggest_edit,is_normal,thumbnail_extra_info,thumbnail,description,content,voteup_count,created,updated,upvoted_followees,voting,review_info,is_labeled,label_info,relationship.is_authorized,voting,is_author,is_thanked,is_nothelp,is_recognized;data[*].author.badge[?(type=best_answerer)].topics'
    
    def start_requests(self):
        yield Request(self.aswer_url.format(fid = self.start_fid,include=self.answer_query),callback=self.parse_page)
        # yield Request(self.follows_url.format(user=self.start_user, include=self.follows_query, offset=0, limit=20),
        #               callback = self.parse_page)

    def parse_page(self,response):
        result = json.loads(response.text)
        item = UserItem()
        for field in item.fields:
            if field in result.keys():
                item[field] = result.get(field)
        yield item
        
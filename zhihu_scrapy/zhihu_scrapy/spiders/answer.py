# -*- coding: utf-8 -*-
import scrapy
import json
from scrapy import Request, Spider
from zhihu_scrapy.items import AnswerItem
import time

class ZhihuAnswerSpider(scrapy.Spider):
    name = 'answer'
    allowed_domains = ['zhihu.com']
    start_urls = ['http://zhihu.com/']
    custom_settings = {
        'MONGO_URI': 'mongodb://answer:asd8561735698@localhost:27017/answer',
        'MONGO_DATABASE': 'answer',
        'ITEM_PIPELINES': {'zhihu_scrapy.pipelines.AnswerPipeline':200}
    }
    aswer_url = 'https://www.zhihu.com/api/v4/favlists/{fid}/items?offset={offset}&include={include}'
    start_fid = '382116557'
    answer_query = 'data[*].created,content.comment_count,suggest_edit,is_normal,thumbnail_extra_info,thumbnail,description,content,voteup_count,created,updated,upvoted_followees,voting,review_info,is_labeled,label_info,relationship.is_authorized,voting,is_author,is_thanked,is_nothelp,is_recognized;data[*].author.badge[?(type=best_answerer)].topics'
    
    def start_requests(self):
        for i in [x for x in range(27) if x % 10 == 0]:
            yield Request(self.aswer_url.format(fid = self.start_fid,offset=i,include=self.answer_query),callback=self.parse_page)
        # yield Request(self.follows_url.format(user=self.start_user, include=self.follows_query, offset=0, limit=20),
        #               callback = self.parse_page)

    def parse_page(self,response):
        result = json.loads(response.text)
        data = result.get('data')
        if data:
            for answer in data:
                yield self.parse_answer(answer)
                
                
    def parse_answer(self,answer):
        created = answer.get('created')
        content = answer.get('content')
        item = AnswerItem()
        for field in item.fields:
            if field in content.keys():
                item[field] = content.get(field)
        item['created'] = created
        yield item
        # paging = result.get('paging')
        # next_url = paging.get('next')
        # print(next_url)
        # yield Request(next_url,callback=self.parse_page)
        
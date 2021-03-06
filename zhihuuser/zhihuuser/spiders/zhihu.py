# -*- coding: utf-8 -*-
import scrapy
import json
from scrapy import Request, Spider
from zhihuuser.items import UserItem
import time

class ZhihuSpider(Spider):
    name = 'zhihu'
    allowed_domains = ['www.zhihu.com']
    start_urls = ['http://www.zhihu.com/']
    follows_url = 'https://www.zhihu.com/api/v4/members/{user}/followers?include={include}&offset={offset}&limit={limit}'
    start_user = 'liang-hao-80'
    follows_query = ('data[*].''locations,gender,educations,business,allow_message,cover_url,following_topic_count,'
                'following_count,thanked_count,voteup_count,following_question_count,'
                'following_favlists_count,following_columns_count,is_followed,pins_count,answer_count,'
                'commercial_question_count,question_count,favorite_count,message_thread_token,'
                'favorited_count,logs_count,marked_answers_count,marked_answers_text,sina_weibo_name,'
                'is_active,account_status,sina_weibo_url,is_bind_sina,is_force_renamed,show_sina_weibo,'
                'is_following,is_blocking,is_blocked,is_org,employments,description,hosted_live_count,'
                'mutual_followees_count,participated_live_count,industry_category,follower_count,'
                'articles_count,org_name,org_homepage,badge[?(type=best_answerer)].topics')
    
    user_url = 'https://www.zhihu.com/api/v4/members/{user}?include={include}'
    user_query = ('locations,gender,educations,business,allow_message,cover_url,following_topic_count,'
              'following_count,thanked_count,voteup_count,following_question_count,'
              'following_favlists_count,following_columns_count,is_followed,pins_count,answer_count,'
              'commercial_question_count,question_count,favorite_count,message_thread_token,'
              'favorited_count,logs_count,marked_answers_count,marked_answers_text,sina_weibo_name,'
              'is_active,account_status,sina_weibo_url,is_bind_sina,is_force_renamed,show_sina_weibo,'
              'is_following,is_blocking,is_blocked,is_org,employments,description,hosted_live_count,'
              'mutual_followees_count,participated_live_count,industry_category,follower_count,'
              'articles_count,org_name,org_homepage,badge[?(type=best_answerer)].topics')
    i = 0
    def start_requests(self):
        yield Request(self.user_url.format(user = self.start_user,include=self.user_query),callback=self.parse_page)
        # yield Request(self.follows_url.format(user=self.start_user, include=self.follows_query, offset=0, limit=20),
        #               callback = self.parse_page)
        
    def parse_page(self,response):
        result = json.loads(response.text)
        follower_count = result['follower_count']
        offset_list = [offset for offset in range(follower_count) if offset % 20 == 0]
        for offset in offset_list:
            print(offset)
            yield Request(self.follows_url.format(user=self.start_user, include=self.follows_query, offset=offset, limit=20),
                        callback = self.parse_follows)
        
    def parse_follows(self, response):
        result1 = json.loads(response.text)
        # if 'paging' in result1.keys() and result1.get('paging').get('is_end') == False:
        #     next_page = result1.get('paging').get('next')
        #     yield Request(next_page, callback=self.parse_follows)
        if 'data' in result1.keys():
            ie = 0
            for result1 in result1.get('data'):
                
                yield Request(self.user_url.format(user=result1.get('url_token'),include=self.user_query), callback=self.parse_user)
                print(ie)
                ie = ie+1
        
    def parse_user(self, response):
        self.i += 1
        print(self.i)
        result = json.loads(response.text)
        item = UserItem()
        for field in item.fields:
            if field in result.keys():
                item[field] = result.get(field)
        
        yield item
import aiohttp
import asyncio
import base64
import execjs
import hmac
import hashlib
import json
import re
import os
import sys
import time
# import threading
from typing import Union
from PIL import Image
from urllib.parse import urlencode
from utils import print_colour
from log import get_logger
from setting import COOKIE_FILE,proxy
from setting import proxy_headers
import detect_captcha
from aiohttp import TCPConnector

count = 0

headers = {
            'Host': 'www.zhihu.com',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 '
                          '(KHTML, like Gecko) Chrome/66.0.3359.181 Safari/537.36',
            #'Connection': 'Keep-Alive',
            'Referer': 'https://www.zhihu.com/',
            'accept-encoding': 'gzip, deflate'
        }
headers.update(proxy_headers)
        

name = 'zhihu'
allowed_domains = ['www.zhihu.com']
start_urls = ['http://www.zhihu.com/']
follows_url = 'https://www.zhihu.com/api/v4/members/{user}/followers?include={include}&offset={offset}&limit={limit}'
start_user = 'xi-feng-du-zi-liang'
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
async def parse_user(session, response):
    # i += 1
    # print(i)
    print(response)        

async def parse_page(session):
        #result = json.loads(response.text)
        #follower_count = result['follower_count']
        offset_list = [0,20,40,60,80]
        pages = []
        for i in offset_list:
            try:
                async with session.get(follows_url.format(user=start_user, include=follows_query, offset=i, limit=20), headers=headers, proxy=proxy, timeout=16) as resp:
                    page = await resp.text()
                    pages.append(page)
            except Exception as e:
                print(e)
        return pages

async def get_user(session, result1):
    
    
    try:
        await asyncio.sleep(2)
        async with session.get(user_url.format(user=result1.get('url_token'),include=user_query), headers=headers, proxy=proxy, timeout=6) as resp:
            text =  await resp.text()
            print(text)
            global count
            print(count)
            count = count + 1
    except Exception as e:
        print(e)       
               
async def parse_follows(session,response):
        result = json.loads(response)
        if 'data' in result.keys():
            users = [get_user(session, result1) for result1 in result.get('data')]
            return await asyncio.wait(users)
      
async def main():
    async with aiohttp.ClientSession(connector=TCPConnector(ssl=False)) as session:
        pages = await parse_page(session)
        taskss = [parse_follows(session,page) for page in pages]
        return await asyncio.wait(taskss)
if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
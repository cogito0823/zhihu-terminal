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
# cookies = 'z_c0="2|1:0|10:1588780750|4:z_c0|80:MS4xaHRkakF3QUFBQUFtQUFBQVlBSlZUYzRzb0Y4dnVULTlwbV8wVGkxcm1BTjJNaDFjUzQ4S3R3PT0=|e7decbe77c86fc792809f11fcf22927d1226de841bef10b113ed623296c8f9ff";'
# #"2|1:0|10:1588780273|4:z_c0|80:MS4xbDlfVkdnQUFBQUFtQUFBQVlBSlZUZkVxb0Y4YV9tUWxqVm9FRXJsb21oUzhzdThaQXdubXZRPT0=|8e514492339d90957bb0e3669aa30c2b21ddd56a6d4fa04a20493ca04e3d3de3"
# #cookies = 'z_c0="2|1:0|10:1588778217|4:z_c0|92:Mi4xaHRkakF3QUFBQUFBb0Z2ZFJBZ1ZFU1lBQUFCZ0FsVk42U0tnWHdEYjJ6TTN5MWlwTWxDb0UtcjdEdHY2QUN4Mzd3|677a24acf7b6acc1add1f9f6d90cc9c98e0d7a03bb3229439a9de83c70456313";'
# headers = {
#     'Host': 'www.zhihu.com',
#     'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 '
#                     '(KHTML, like Gecko) Chrome/66.0.3359.181 Safari/537.36',
#     #'Connection': 'Keep-Alive',
#     'Referer': 'https://www.zhihu.com/',
#     'accept-encoding' : 'gzip, deflate',
#     # 'accept-language' : 'zh-CN,zh;q=0.9',
#     # 'cache-control' : 'no-cache',
#     'cookie' : cookies,
#     #'pragma' : 'no-cache',
#     #'referer' : 'https://www.zhihu.com/follow',
#     # 'sec-fetch-dest' : 'empty',
#     # 'sec-fetch-mode' : 'cors',
#     # 'sec-fetch-site' : 'same-origin',
#     #'user-agent' : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.129 Safari/537.36',
#     # 'x-ab-param' : 'tp_club_flow_ai=0;pf_fuceng=1;pf_newguide_vertical=0;zr_slot_training=2;zr_search_topic=0;zr_intervene=0;soc_iosweeklynew=0;pf_foltopic_usernum=50;li_svip_tab_search=1;li__edu_cold_start=1;zr_answer_rec_cp=open;se_dnn_mt_v2=0;top_universalebook=1;qap_article_like=1;se_adsrank=0;se_col_boost=0;se_page_quality=1;se_v040=0;se_backsearch=0;se_cbert_index=1;zr_km_answer=open_cvr;tp_meta_card=0;top_root=0;tp_club_join=1;zr_zr_search_sims=0;tp_club_tab_feed=0;se_college=default;tp_sft_v2=d;top_ydyq=X;li_salt_hot=1;li_paid_answer_exp=0;se_topicfeed=0;top_ebook=0;tsp_videobillboard=7;se_v039=0;se_cardrank_4=1;tp_topic_tab=0;tp_m_intro_re_topic=1;qap_question_author=0;zr_expslotpaid=1;se_v038=0;li_ebok_chap=0;se_searchwiki=0;se_highlight_online=0;pf_profile2_tab=0;ug_goodcomment_0=1;li_topics_search=0;li_viptab_name=0;se_relation_1=2;se_searchvideo=0;li_yxzl_new_style_a=1;zr_art_rec=base;tp_topic_rec=1;soc_adweeklynew=0;se_whitelist=1;se_clarify=0;li_assessment_show=1;tp_club_feed=1;zr_training_boost=false;se_specialbutton=0;tp_topic_tab_new=0-0-0;ls_recommend_test=0;tp_club_android_feed=old;top_quality=0;ug_follow_topic_1=2;se_hotsearch_2=1;ug_newtag=1;tp_topic_style=0;ls_videoad=2;li_vip_verti_search=0;se_highlight=1;se_cardrank_3=0;zr_slotpaidexp=8;tsp_hotlist_ui=3;ls_video_commercial=0;li_hot_voted=0;se_hotmore=2;tp_sft=a;qap_question_visitor= 0;se_club_boost=1;tp_score_1=a;li_answers_link=0;qap_labeltype=1;se_content0=1;se_ffzx_jushen1=0;ls_fmp4=0;zr_rel_search=base;se_cardrank_2=1;se_clubrank=1;tp_club_qa_entrance=0;li_se_section=1;zr_ans_rec=gbrank;se_colorfultab=1;top_test_4_liguangyi=1;pf_noti_entry_num=0;li_answer_card=0;tp_topic_entry=0;tp_move_scorecard=0;li_catalog_card=1;zr_slot_up2=1;pf_creator_card=1;tp_discovery_ab_1=0;tp_header_style=1;soc_notification=1;li_answer_test=3;qap_thanks=1;zr_article_new=close;se_hotsearch=1;tp_discover_copy=0;top_v_album=1;li_svip_cardshow=1;li_video_section=1;li_training_chapter=0;se_billboardsearch=0;se_multianswer=2;tp_topic_head=0;top_hotcommerce=1;zr_training_first=false;se_faxian_jiahao=0;tp_club_entrance=1;se_expired_ob=0;zr_search_paid=1;zr_rec_answer_cp=open;tp_discover=1;zr_test_aa1=1;se_aa_base=0;se_sug_term=0;tp_club_tab=0;tp_movie_ux=0;li_answer_test_2=0;li_ebook_gen_search=2;zw_sameq_sorce=999;pf_adjust=0',
#     # 'x-api-version' : '3.0.53',
#     # 'x-requested-with' : 'fetch',
#     # 'x-zse-83' : '3_2.0',
#     #'x-zse-86' : '1.0_a7YBeTuyNBSYU9xyBTO024u0ggYf6L28sHYqHreqr02X',
#     #'x-zst-81' : '3_2.0ae3TnRUTEvOOUCNMTQnTSHUZo02p-HNMZBO8YD_ykXtue_t0K6P0EAuy-LS9-hp1DufI-we8gGHPgJO1xuPZ0GxCTJHR7820XM20cLRGDJXfgGCBxupMuD_Ie8FL7AtqM6O1VDQyQ6nxrRPCHukMoCXBEgOsiRP0XL2ZUBXmDDV9qhnyTXFMnXcTF_ntRueThMtYEvHYiqLVZGN1zceLLqO9LwtxyvLBF9cmo6Vqtqg_Pgc9Eug_wqofp9YPv4NqduoC1crMbMYmZhXMhuVOIDuC0wYpb02CfX2mebLf-gpVBggLQcS0jr3C2JSXcQNmt92BwBSYxC3mAGOZm0wMcDrYn9gKVvwfEgFC3JcV-JO1Futm5qfz-rrL3gx8S0pB8CXfODc8iUtM2MwYmLt0XcOyrHeXNBXyYBVL67O8aqtL8qOO17YqxgrBrR2m0GX1pXeB3GQ0n9Sur4eqEbH8khx9r7VVQB2muwHCuJUC',
# }

# url = 'https://www.zhihu.com/api/v3/moments?'
# data = {
#     'desktop': 'true',
#     'limit': '6',
# }

# async def main():
#     async with aiohttp.ClientSession(connector=TCPConnector(ssl=False)) as session:
#         async with session.get('https://www.zhihu.com/api/v3/moments?', params=data, proxy=proxy, headers=headers) as resp:
#             result = await resp.json()
#             return result
            
# loop = asyncio.get_event_loop()
# loop.run_until_complete(main())
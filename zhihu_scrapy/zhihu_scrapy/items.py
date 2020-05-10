# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

from scrapy import Item, Field

class UserItem(Item):
    # define the fields for your item here like:
    id = Field()
    name = Field()
    avatar_url = Field()
    headline = Field()
    description = Field()
    url = Field()
    url_token = Field()
    gender = Field()
    cover_url = Field()
    type = Field()
    badge = Field()
    
    employments = Field()
    locations = Field()
    educations = Field()
    
    business = Field()
    allow_message = Field()
    following_topic_count = Field()
    following_count = Field()
    thanked_count = Field()
    voteup_count = Field()
    following_question_count = Field()
    following_favlists_count = Field()
    following_columns_count = Field()
    is_followed = Field()
    pins_count = Field()
    commercial_question_count = Field()
    question_count = Field()
    favorite_count = Field()
    message_thread_token = Field()
    favorited_count = Field()
    logs_count = Field()
    marked_answers_count = Field()
    marked_answers_text = Field()
    sina_weibo_name = Field()
    is_active = Field()
    account_status = Field()
    sina_weibo_url = Field()
    is_bind_sina = Field()
    is_force_renamed = Field()
    show_sina_weibo = Field()
    is_following = Field()
    is_blocking = Field()
    is_blocked = Field()
    is_org = Field()
    hosted_live_count = Field()
    mutual_followees_count = Field()
    participated_live_count = Field()
    industry_category = Field()
    follower_count = Field()
    articles_count = Field()
    org_name = Field()
    org_homepage = Field()


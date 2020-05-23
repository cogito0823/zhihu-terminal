from spider.spiderBaseclass import SpiderBaseclass
from setting import proxy

class UserSpider(SpiderBaseclass):
    """用户信息爬取"""
    async def get_self_info(self) -> dict:
        """
        获取我的信息
        :return:
        """
        url = 'https://www.zhihu.com/api/v4/me?include=ad_type;available_message_types,' \
              'default_notifications_count,follow_notifications_count,vote_thank_notifications_count,' \
              'messages_count;draft_count;following_question_count;account_status,is_bind_phone,' \
              'is_force_renamed,email,renamed_fullname;ad_type'

        async with self.client.get(url, proxy=proxy) as resp:
            result = await resp.json()
            self.logger.debug(result)
        return result
    
    async def get_user_info(self, url_token) -> dict:
        """
        获取我的信息
        :return:
        """
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
        try:
            async with self.client.get(user_url.format(user=url_token, include=user_query), proxy=proxy) as resp:
                result = await resp.json()
                self.logger.debug(result)
            return result
        except:
            return False
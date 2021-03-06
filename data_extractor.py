"""
处理从知乎获取到的数据,去除不需要的数据
"""
import json
from pyquery import PyQuery as pq
from spider.article_spider import ArticleSpider
from spider.comment_spider import CommentSpider
from spider.user_spider import UserSpider


class DataExtractor(ArticleSpider, CommentSpider, UserSpider):
    """数据提取"""
    
# ========================== 用户 ===============================

    async def get_user_info(self, url_token):
        result = await super().get_user_info(url_token)
        if not result:
            return False
        elif result.get('error'):
            return False
        return result
    
    async def get_self_info(self) -> dict:
        """
        获取自己的信息
        :return:
        """
        result = await super().get_self_info()
        output = {
            'name': result['name'],
            'haealine': result['headline'],
            'head': result['avatar_url'],
            'gender': result['gender'],
            'vip_info': result['vip_info'],
            'url': result['url'],
        }
        self.logger.debug(output)
        return output

# ========================= 展示页  =============================

    async def get_recommend_article(self) -> list:
        """
        获取推荐文章
        :return:
        """
        result = await super().get_recommend_article()
        output = []
        for d in result['data']:  # 提取用到的数据
            target = d['target']
            if target['type'] == 'question_ask':
                continue
            author = target['author']
            question = target.get('question')
            playlist = target.get('thumbnail_extra_info', {}).get('playlist')
            article_info = {
                'author': {  # 作者信息
                    'name': author['name'],
                    'headline': author.get('headline'),
                    'head': author['avatar_url'],
                    'gender': author.get('gender'),
                    'url': author.get('url'),
                    'url_token': author.get('url_token')
                },
                'excerpt': target.get('excerpt_new') or target.get('excerpt'),
                'content': target['content'],
                'voteup_count': target.get('voteup_count', target.get('vote_count')),  # 赞同数
                'visited_count': target.get('visited_count'),
                'thanks_count': target.get('thanks_count', 0),
                'comment_count': target['comment_count'],
                'id': str(target['id']),
                'type': target['type'],
                'created_time': d['created_time'],
                'updated_time': d['updated_time'],
            }
            # # 如果type是zvideo，那么voteup_count对应的属性名是vote_count,这里把属性名修改过来
            if target['type'] == 'zvideo' and playlist:
                article_info['content'] += f'\n{playlist.get("hd", {}).get("url", "")}'
                article_info['excerpt'] = '**video**'
            #     article_info['voteup_count'] = target.get('vote_count')
            if question:
                question = {
                    'author': {
                        'name': question['author']['name'],
                        'headline': question['author'].get('headline'),
                        'head': question['author'].get('head'),
                        'gender': question['author'].get('gender'),
                        'url': question['author'].get('url'),
                    },
                    'title': question['title'],
                    'url': question['url'],
                    'id': str(question['id']),
                    'type': 'normal',
                }
            else:
                question = {
                    'title': target['title'],
                    'url': target.get('url'),
                    'type': 'market',
                    'id': '',
                    'author': target['author']
                }
            article_info['question'] = question
            output.append(article_info)
        self.logger.debug(output)
        return output

    async def get_aten_article(self, *next_url) -> list:
        """
        获取推荐文章
        :return:
        """
        if next_url:  
            result = await super().get_aten_article(next_url[0])
        else:
            result = await super().get_aten_article()
        output = []
        for d in result['data']:  # 提取用到的数据
            if not 'target' in d.keys():
                continue
            target = d['target']
            if target['type'] == 'question':
                continue
            if target['type'] == 'roundtable':
                continue
            if target['type'] == 'column':
                continue
            author = target['author']
            question = target.get('question')
            playlist = target.get('thumbnail_extra_info', {}).get('playlist')
            article_info = {
                'author': {  # 作者信息
                    'name': author['name'],
                    'headline': author.get('headline'),
                    'head': author['avatar_url'],
                    'gender': author.get('gender'),
                    'url': author.get('url'),
                    'url_token': author.get('url_token')
                },
                'excerpt': target.get('excerpt_new') or target.get('excerpt'),
                'content': target['content'],
                'voteup_count': target.get('voteup_count', target.get('vote_count')),  # 赞同数
                'visited_count': target.get('visited_count'),
                'thanks_count': target.get('thanks_count', 0),
                'comment_count': target['comment_count'],
                'id': str(target['id']),
                'type': target['type'],
                'actors': d['actors'],
                'action_text_tpl': d['action_text_tpl'],
                'created_time': d['created_time'],
                'updated_time': d['updated_time'],
            }
            # # 如果type是zvideo，那么voteup_count对应的属性名是vote_count,这里把属性名修改过来
            if target['type'] == 'zvideo' and playlist:
                article_info['content'] += f'\n{playlist.get("hd", {}).get("url", "")}'
                article_info['excerpt'] = '**video**'
            #     article_info['voteup_count'] = target.get('vote_count')
            if question:
                question = {
                    'author': {
                        'name': question['author']['name'],
                        'headline': question['author'].get('headline'),
                        'head': question['author'].get('head'),
                        'gender': question['author'].get('gender'),
                        'url': question['author'].get('url'),
                    },
                    'title': question['title'],
                    'url': question['url'],
                    'id': str(question['id']),
                    'type': 'normal',
                }
            else:
                question = {
                    'title': target['title'],
                    'url': target.get('url'),
                    'type': 'market',
                    'id': '',
                    'author': target['author']
                }
            article_info['question'] = question
            output.append(article_info)
        paging = result['paging']
        output.append(paging)
        self.logger.debug(output)
        return output

    async def get_act_article(self,url_token, *next_url):
        """
        获取动态文章
        :return:
        """
        if next_url:  
            result = await super().get_act_article(url_token, next_url[0])
        else:
            result = await super().get_act_article(url_token)
        output = []
        for d in result['data']:  # 提取用到的数据
            if not 'target' in d.keys():
                continue
            action_text_tpl = d.get('action_text')
            target = d['target']
            if target['type'] == 'question':
                continue
            if target['type'] == 'roundtable':
                continue
            if target['type'] == 'column':
                continue
            author = target['author']
            question = target.get('question')
            playlist = target.get('thumbnail_extra_info', {}).get('playlist')
            article_info = {
                'author': {  # 作者信息
                    'name': author['name'],
                    'headline': author.get('headline'),
                    'head': author['avatar_url'],
                    'gender': author.get('gender'),
                    'url': author.get('url'),
                    'url_token': author.get('url_token')
                },
                'excerpt': target.get('excerpt_new') or target.get('excerpt'),
                'content': target['content'],
                'voteup_count': target.get('voteup_count', target.get('vote_count')),  # 赞同数
                'visited_count': target.get('visited_count'),
                'thanks_count': target.get('thanks_count', 0),
                'comment_count': target['comment_count'],
                'id': str(target['id']),
                'type': target['type'],
                'action_text_tpl': action_text_tpl,
                'created_time': d['created_time'],
            }
            # # 如果type是zvideo，那么voteup_count对应的属性名是vote_count,这里把属性名修改过来
            if target['type'] == 'zvideo' and playlist:
                article_info['content'] += f'\n{playlist.get("hd", {}).get("url", "")}'
                article_info['excerpt'] = '**video**'
            #     article_info['voteup_count'] = target.get('vote_count')
            if question:
                question = {
                    'author': {
                        'name': question['author']['name'],
                        'headline': question['author'].get('headline'),
                        'head': question['author'].get('head'),
                        'gender': question['author'].get('gender'),
                        'url': question['author'].get('url'),
                    },
                    'title': question['title'],
                    'url': question['url'],
                    'id': str(question['id']),
                    'type': 'normal',
                }
            else:
                question = {
                    'title': target['title'],
                    'url': target.get('url'),
                    'type': 'market',
                    'id': '',
                    'author': target['author']
                }
            article_info['question'] = question
            output.append(article_info)
        paging = result['paging']
        output.append(paging)
        self.logger.debug(output)
        return output
    
    async def get_items_article(self, fid='114929484', *next_url):
        if next_url:  
            result = await super().get_items_article(fid, next_url[0])
        else:
            result = await super().get_items_article(fid)
        output = []
        for d in result['data']:  # 提取用到的数据
            created = d.get("created")
            if not 'content' in d.keys():
                continue
            target = d['content']
            if target['type'] == 'question':
                continue
            if target['type'] == 'roundtable':
                continue
            if target['type'] == 'column':
                continue
            author = target['author']
            question = target.get('question')
            playlist = target.get('thumbnail_extra_info', {}).get('playlist')
            article_info = {
                'author': {  # 作者信息
                    'name': author['name'],
                    'headline': author.get('headline'),
                    'head': author['avatar_url'],
                    'gender': author.get('gender'),
                    'url': author.get('url'),
                    'url_token': author.get('url_token')
                },
                'excerpt': target.get('excerpt_new') or target.get('excerpt'),
                'content': target['content'],
                'voteup_count': target.get('voteup_count', target.get('vote_count')),  # 赞同数
                'comment_count': target['comment_count'],
                'id': str(target['id']),
                'type': target['type'],
                'created_time': created,
            }
            # # 如果type是zvideo，那么voteup_count对应的属性名是vote_count,这里把属性名修改过来
            if target['type'] == 'zvideo' and playlist:
                article_info['content'] += f'\n{playlist.get("hd", {}).get("url", "")}'
                article_info['excerpt'] = '**video**'
            #     article_info['voteup_count'] = target.get('vote_count')
            if question:
                question = {
                    'title': question['title'],
                    'url': question['url'],
                    'id': str(question['id']),
                    'type': 'normal',
                }
            else:
                question = {
                    'title': target['title'],
                    'url': target.get('url'),
                    'type': 'market',
                    'id': ''
                }
            article_info['question'] = question
            output.append(article_info)
        paging = result['paging']
        output.append(paging)
        self.logger.debug(output)
        return output
    
    async def get_fav_list(self, url_token='hua-chen-15-43-10', *next_url):
        result = await super().get_fav_list(url_token)
        print(result)
        
# ========================== 评论 ===============================

    def extract_comments(self, result: dict) -> tuple:
        """
        提取评论
        :param result:
        :return:
        """
        output = []
        for d in result['data']:
            author = d['author']['member']
            for clild in d['child_comments']:
                clild['author'] = clild['author']['member']
                if clild['reply_to_author'].get('member'):
                    clild['reply_to_author'] = clild['reply_to_author']['member']
            if not d.get('reply_to_author', {}):
                reply_to_author = {}
            else:
                reply_to_author = d.get('reply_to_author', {}).get('member', {})
            comment_info = {
                'author': {
                    'name': author.get('name'),
                    'headline': author.get('headline'),
                    'head': author.get('head'),
                    'gender': author.get('gender'),
                    'url': author.get('url'),
                },
                'content': d['content'],
                'created_time': d['created_time'],
                'child_comment_count': d['child_comment_count'],
                'id': str(d['id']),
                'vote_count': d['vote_count'],
                'voting': d['voting'],
                'type': d['type'],
                'featured': d.get('featured'),  # 是否是热评
                'reply_to_author': {
                    'name': reply_to_author.get('name'),
                    'headline': reply_to_author.get('headline'),
                    'head': reply_to_author.get('head'),
                    'gender': reply_to_author.get('gender'),
                    'url': reply_to_author.get('url'),
                },
                'child_comments': d['child_comments']
            }
            output.append(comment_info)
        self.logger.debug(output)
        paging = result['paging']
        return output, paging

    async def get_comments(self, uid: str, typ: str ='answer') -> tuple:
        """
        获取评论
        :param typ:
        :param uid:
        :return:
        """
        result = await super().get_comments(uid, typ)
        output, paging = self.extract_comments(result)
        return output, paging

    async def get_comments_by_url(self, url: str) -> tuple:
        """
        获取评论
        :return:
        """
        result = await super().get_comments_by_url(url)
        output, paging = self.extract_comments(result)
        return output, paging

# ========================== 问题 ===============================

    async def get_question_details(self, question_id: str, uid: str) -> dict:
        """
        获取评论
        :return:
        """
        result = await super().get_question_article_first(question_id, uid)
        doc = pq(result)
        data = doc('#js-initialData').text()
        result = json.loads(data)
        questions = list(result['initialState']['entities']['questions'].values())[0]
        # answers = list(result['initialState']['entities']['answers'].values())[0]
        output = {
                'id': questions['id'],
                'type': questions['type'],
                'title': questions['title'],
                'creTime': questions.get('creTime') or questions.get('created'),
                'excerpt': questions['excerpt'],
                'detail': questions['detail'],
                'author': questions['author'],
                'answerCount': questions['answerCount'],
                'visitCount': questions['visitCount'],
                'comment_count': questions['commentCount'],
                'followerCount': questions['followerCount'],
        }
        return output

    def extract_article_by_question(self, result):
        """
        提取文章信息
        :param result:
        :return:
        """
        output = []
        for d in result['data']:  # 提取用到的数据
            target = d
            author = target['author']
            question = target.get('question')
            article_info = {
                'author': {  # 作者信息
                    'name': author['name'],
                    'headline': author.get('headline'),
                    'head': author['avatar_url'],
                    'gender': author.get('gender'),
                    'url': author.get('url'),
                    'url_token': author.get('url_token')
                },
                'excerpt': target.get('excerpt_new') or target.get('excerpt'),
                'content': target['content'],
                'voteup_count': target['voteup_count'],  # 赞同数
                'visited_count': target.get('visited_count', 0),
                'thanks_count': target.get('thanks_count', 0),
                'comment_count': target['comment_count'],
                'id': str(target['id']),
                'type': target['type'],
                'created_time': d['created_time'],
                'updated_time': d['updated_time'],
            }
            if question:
                question = {
                    'title': question['title'],
                    'url': question['url'],
                    'id': str(question['id']),
                    'type': 'normal',
                }
            else:
                question = {
                    'title': target['title'],
                    'url': target['url'],
                    'type': 'market',
                    'id': '',
                }
            article_info['question'] = question
            output.append(article_info)
        return output

    async def get_article_by_question(self, question_id, offset: int = 0, limit: int = 3) -> tuple:
        """
        :param question_id:
        :param offset:
        :param limit:
        :return:
        """
        result = await super().get_article_by_question(question_id, offset, limit)
        output = self.extract_article_by_question(result)
        paging = result['paging']
        self.logger.debug(output)
        return output, paging

    async def get_article_by_question_url(self, url):
        """
        :param url:
        :return:
        """
        result = await super().get_article_by_question_url(url)
        output = self.extract_article_by_question(result)
        paging = result['paging']
        self.logger.debug(output)
        return output, paging

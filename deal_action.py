import os

from print_beautify import print_colour
from print_beautify import print_recommend_article
from print_beautify import print_aten_article 
from print_beautify import print_vote_comments 
from print_beautify import print_article_content 
from print_beautify import print_article_content
from print_beautify import print_article_content 
from print_beautify import print_comments 
from print_beautify import print_vote_thank 
from print_beautify import print_question
from print_beautify import print_save
from print_beautify import print_user_info
from print_beautify import print_act_article
from print_beautify import print_items_article
from print_beautify import print_fav_list
from help_menu import help_recommend 
from help_menu import help_aten 
from help_menu import help_act
from help_menu import help_comments 
from help_menu import help_comments2 
from help_menu import help_question
from help_menu import help_article
from help_menu import help_user
from help_menu import help_item

async def app_exit(cmd: str, spider=False):
    if cmd in('q', 'quit', 'exit'):
        if spider:
            await spider.client.close()
        os._exit(0)

cmd_func_map = {
    'up': 'endorse_answer',
    'down': 'endorse_answer',
    'neutral': 'endorse_answer',
    'thank': 'thank_answer',
    'unthank': 'thank_answer',
    'read-cmt': 'get_comments',
}

def get_com_func(cmd):
    return cmd_func_map[cmd]

# ========================== 用户 ===============================

async def deal_user(spider, url_token):
    is_print = True
    while True:
        if is_print:
            user_info = await spider.get_user_info(url_token)
            if user_info == False:
                break
            print_user_info(user_info)
            is_print = False
        print_colour('', 'yellow')
        remd_cmd = input(help_user()).lower()
        remd_cmd = remd_cmd.split(':')
        if not remd_cmd:
            print_colour('输入有误!', 'red')
            continue
        await app_exit(remd_cmd[0], spider)
        if remd_cmd[0] == 'r':
            print_user_info(user_info)
            continue
        elif remd_cmd[0] == "act":
            await deal_act(spider,url_token)
            continue
        elif remd_cmd[0] == "fav":
            # await deal_fav(spider,url_token)
            continue
        elif remd_cmd[0] == 'question':
            question_ids = [d.get('question').get('id') for d in user_info]
            if len(remd_cmd) != 2:
                print_colour('输入有误!', 'red')
                continue
            if remd_cmd[1] not in question_ids:
                print_colour('输入id有误!', 'red')
                continue
            continue
        elif remd_cmd[0] == 'back':
            break
        else:
            print_colour('输入有误!', 'red')
            continue
        
# ========================== 评论 ===============================

async def deal_comments_by_id(spider, uid):
    """
    对应id评论相关
    :param spider:
    :return:
    """
    while True:
        print_colour('', 'yellow')
        com2_cmd = input(help_comments2()).lower()
        com2_cmd = com2_cmd.split(':')
        if not com2_cmd[0]:
            print_colour('输入有误!', 'red')
            continue
        app_exit(com2_cmd[0], spider)
        if com2_cmd[0] == 'back':
            break
        elif com2_cmd[0] == 'up':
            result = await spider.endorse_comment(uid, False)
            print_vote_comments(result, 'up')
        elif com2_cmd[0] == 'neutral':
            result = await spider.endorse_comment(uid, True)
            print_colour(result)
            print_vote_comments(result, 'neutral')
        elif com2_cmd[0] == 'reply' and len(com2_cmd) == 2:
            print_colour('功能还在开发中...', 'red')
            continue
        else:
            print_colour('输入有误!', 'red')
            continue
    pass

async def deal_comments(spider, result, paging):
    """
    处理评论命令
    :param spider:
    :return:
    """
    while True:
        comment_ids = []
        for d in result:
            comment_ids.append(d['id'])
            for clild in d.get('child_comments'):
                comment_ids.append(clild['id'])
        comment_ids = list(set(comment_ids))
        print_colour('', 'yellow')
        comm_cmd = input(help_comments()).lower()
        comm_cmd = comm_cmd.split(':')
        if not comm_cmd:
            print_colour('输入有误!', 'red')
            continue
        await app_exit(comm_cmd[0], spider)
        if comm_cmd[0] == 'back':
            break
        elif comm_cmd[0] == 'r':
            print_comments(result)
            continue
        elif comm_cmd[0] == 'n':
            if paging.get('is_end'):
                print_colour('已是最后一页!', 'red')
                continue
            url = paging['next']
            result, paging = await spider.get_comments_by_url(url)
            print_comments(result)
            continue
        elif comm_cmd[0] == 'p':
            if paging.get('is_start'):
                print_colour('已是第一页!', 'red')
                continue
            url = paging['previous']
            result, paging = await spider.get_comments_by_url(url)
            print_comments(result)
            continue
        elif comm_cmd[0] == 'com':
            if len(comm_cmd) != 2:
                print_colour('输入有误!', 'red')
                continue
            if comm_cmd[1] not in comment_ids:
                print_colour('输入id有误!', 'red')
                continue
            await deal_comments_by_id(spider, comm_cmd[1])
            continue
        else:
            print_colour('输入有误!', 'red')
            continue

# ========================== 文章 ===============================

async def deal_article(spider, article):
    """
    处理文章内容命令
    :param spider:
    :param recommend_articles:
    :param ids:
    :return:
    """
    while True:
        print_colour('', 'yellow')
        arl_cmd = input(help_article()).lower()
        if not arl_cmd:
            print_colour('输入有误!', 'red')
            continue
        await app_exit(arl_cmd, spider)
        if arl_cmd == 'back':
            break
        
        elif arl_cmd == 'r':
            print_article_content(article)
            continue
        elif arl_cmd in ('up', 'down', 'neutral', 'thank', 'unthank'):

            uid = article.get('id')
            func = get_com_func(arl_cmd)
            result = await getattr(spider, func)(uid)
            print_vote_thank(result, arl_cmd)
            continue
        elif arl_cmd == 'comment':
            typ = article['type']
            uid = article.get('id')
            result, paging = await spider.get_comments(uid, typ)
            print_comments(result)
            await deal_comments(spider, result, paging)
            continue
        elif arl_cmd == 'save':
            print_save(article)
            continue
        elif arl_cmd == 'enshrine':
            print_colour('功能还在开发中...', 'red')
            continue
        elif arl_cmd == 'question':
            await deal_question(spider, article.get('question').get('id'), article.get('id'))
            continue
        else:
            print_colour('输入有误!', 'red')
            continue

# ========================== 问题 ===============================

async def deal_question(spider, question_id, uid):
    """
    处理问题命令
    :param spider:
    :param uid:
    :param id_map:
    :return:
    """
    is_print = True
    while True:
        if is_print:
            question_articles, paging = await spider.get_article_by_question(question_id)
            ids = [d.get('id') for d in question_articles]
            print_recommend_article(question_articles)
            is_print = False
        print_colour('', 'yellow')
        ques_cmd = input(help_question()).lower()
        ques_cmd = ques_cmd.split(':')
        if not ques_cmd:
            print_colour('输入有误!', 'red')
            continue
        await app_exit(ques_cmd[0], spider)
        if ques_cmd[0] == 'read':
            if len(ques_cmd) != 2:
                print_colour('输入有误!', 'red')
                continue
            if ques_cmd[1] not in ids:
                print_colour('输入id有误!', 'red')
                continue
            output = [d for d in question_articles if d['id'] == ques_cmd[1]][0]
            print_article_content(output)
            await deal_article(spider, output)
            continue
        elif ques_cmd[0] == 'qsdl':
            question_detail = await spider.get_question_details(question_id, uid)
            print_question(question_detail)
        elif ques_cmd[0] == 'n':
            if paging.get('is_end'):
                print_colour('已是最后一页!', 'red')
                continue
            url = paging['next']
            question_articles, paging = await spider.get_article_by_question_url(url)
            ids = [d.get('id') for d in question_articles]
            print_recommend_article(question_articles)
            continue
        elif ques_cmd[0] == 'p':
            if paging.get('is_start'):
                print_colour('已是第一页!', 'red')
                continue
            url = paging['previous']
            question_articles, paging = await spider.get_article_by_question_url(url)
            ids = [d.get('id') for d in question_articles]
            print_recommend_article(question_articles)
        elif ques_cmd[0] == 'r':
            print_recommend_article(question_articles)
            continue
        elif ques_cmd[0] == 'back':
            break
        else:
            print_colour('输入有误!', 'red')
            continue

# ========================== 展示 ===============================

class RemdPage ():
    @classmethod
    async def create(cls, spider):
        self = RemdPage()
        self.recommend_articles = await spider.get_recommend_article()
        return self
    async def deal_remd(self, spider):
        """
        处理推荐文章命令
        :param spider:
        :return:
        """
        is_print = True
        while True:
            if is_print:
                is_print = False
                recommend_articles = self.recommend_articles
                ids = [d.get('id') for d in recommend_articles]
                print_recommend_article(recommend_articles)
            print_colour('', 'yellow')
            remd_cmd = input(help_recommend())
            remd_cmd = remd_cmd.split(':')
            if not remd_cmd:
                print_colour('输入有误!', 'red')
                continue
            await app_exit(remd_cmd[0], spider)
            if remd_cmd[0] == 'f':
                is_print = True
                self.recommend_articles = await spider.get_recommend_article()
                continue
            elif remd_cmd[0] == 'r':
                print_recommend_article(recommend_articles)
                continue
            elif remd_cmd[0] == 'user':
                user_info = await spider.get_user_info(remd_cmd[1])
                if user_info == False:
                    print_colour('用户不存在或url_token输入有误!', 'red')
                    continue
                await deal_user(spider, remd_cmd[1])
                continue
            elif remd_cmd[0] == 'read':
                if len(remd_cmd) != 2:
                    print_colour('输入有误!', 'red')
                    continue
                if remd_cmd[1] not in ids:
                    print_colour('输入id有误! 请检查id是否在此页', 'red')
                    continue
                output = [d for d in recommend_articles if d['id'] == remd_cmd[1]][0]
                print_article_content(output)
                await deal_article(spider, output)
                continue
            elif remd_cmd[0] == 'question':
                question_ids = [d.get('question').get('id') for d in recommend_articles]
                if len(remd_cmd) != 2:
                    print_colour('输入有误!', 'red')
                    continue
                if remd_cmd[1] not in question_ids:
                    print_colour('输入id有误!', 'red')
                    continue
                assert len(ids) == len(question_ids)
                id_map = dict(zip(question_ids, ids))
                uid = id_map[remd_cmd[1]]
                await deal_question(spider, remd_cmd[1], uid)
                continue
            elif remd_cmd[0] == 'back':
                break
            else:
                print_colour('输入有误!', 'red')
                continue

class AtenPage():
    @classmethod
    async def create(cls, spider):
        self = AtenPage()
        self.aten_articles = await spider.get_aten_article()
        return self
    async def deal_aten(self, spider):
        """
        处理推荐文章命令
        :param spider:
        :return:
        """
        is_next = False
        is_print = True
        paging = {}
        while True:
            if is_print:
                if is_next:
                    next_url = paging['next']
                    self.aten_articles = await spider.get_aten_article(next_url)
                    aten_articles = self.aten_articles[:]
                    paging = aten_articles.pop(-1)
                    ids = [d.get('id') for d in aten_articles]
                    print_aten_article(aten_articles)
                else:
                    aten_articles = self.aten_articles[:]
                    paging = aten_articles.pop(-1)
                    ids = [d.get('id') for d in aten_articles]
                    print_aten_article(aten_articles)
                is_print = False
                is_next = False
            print_colour('', 'yellow')
            aten_cmd = input(help_aten())
            aten_cmd = aten_cmd.split(':')
            if not aten_cmd:
                print_colour('输入有误!', 'red')
                continue
            await app_exit(aten_cmd[0], spider)
            if aten_cmd[0] == 'f':
                is_print = True
                self.aten_articles = await spider.get_aten_article()
                continue
            elif aten_cmd[0] == 'r':
                print_aten_article(aten_articles)
                continue
            elif aten_cmd[0] == 'n':
                if paging.get('is_end'):
                    print_colour('已是第一页!', 'red')
                    continue
                is_print = True
                is_next = True
                continue
            elif aten_cmd[0] == 'user':
                user_info = await spider.get_user_info(aten_cmd[1])
                if user_info == False:
                    print_colour('用户不存在或url_token输入有误!', 'red')
                    continue
                await deal_user(spider, aten_cmd[1])
                continue
            elif aten_cmd[0] == 'read':
                if len(aten_cmd) != 2:
                    print_colour('输入有误!', 'red')
                    continue
                if aten_cmd[1] not in ids:
                    print_colour('输入id有误! 请检查id是否在此页', 'red')
                    continue
                output = [d for d in aten_articles if d['id'] == aten_cmd[1]][0]
                print_article_content(output)
                await deal_article(spider, output)
                continue
            elif aten_cmd[0] == 'question':
                question_ids = [d.get('question').get('id') for d in aten_articles]
                if len(aten_cmd) != 2:
                    print_colour('输入有误!', 'red')
                    continue
                if aten_cmd[1] not in question_ids:
                    print_colour('输入id有误!', 'red')
                    continue
                assert len(ids) == len(question_ids)
                id_map = dict(zip(question_ids, ids))
                uid = id_map[aten_cmd[1]]
                await deal_question(spider, aten_cmd[1], uid)
                continue
            elif aten_cmd[0] == 'back':
                break
            else:
                print_colour('输入有误!', 'red')
                continue

async def deal_act(spider,url_token):
    """
    处理推荐文章命令
    :param spider:
    :return:
    """
    is_next = False
    is_print = True
    paging = {}
    while True:
        if is_print:
            if is_next:
                next_url = paging['next']
                aten_articles = await spider.get_act_article(url_token, next_url)
                paging = aten_articles.pop(-1)
                ids = [d.get('id') for d in aten_articles]
                print_act_article(aten_articles)
            else:
                aten_articles = await spider.get_act_article(url_token)
                paging = aten_articles.pop(-1)
                ids = [d.get('id') for d in aten_articles]
                print_act_article(aten_articles)
            is_print = False
            is_next = False
        print_colour('', 'yellow')
        aten_cmd = input(help_act()).lower()
        aten_cmd = aten_cmd.split(':')
        if not aten_cmd:
            print_colour('输入有误!', 'red')
            continue
        await app_exit(aten_cmd[0], spider)
        if aten_cmd[0] == 'f':
            is_print = True
            continue
        elif aten_cmd[0] == 'r':
            print_act_article(aten_articles)
            continue
        elif aten_cmd[0] == 'n':
            if paging.get('is_end'):
                print_colour('已是第一页!', 'red')
                continue
            is_print = True
            is_next = True
            continue
        elif aten_cmd[0] == 'user':
            user_info = await spider.get_user_info(aten_cmd[1])
            if user_info == False:
                print_colour('用户不存在或url_token输入有误!', 'red')
                continue
            await deal_user(spider, aten_cmd[1])
            continue
        elif aten_cmd[0] == 'read':
            if len(aten_cmd) != 2:
                print_colour('输入有误!', 'red')
                continue
            if aten_cmd[1] not in ids:
                print_colour('输入id有误! 请检查id是否在此页', 'red')
                continue
            output = [d for d in aten_articles if d['id'] == aten_cmd[1]][0]
            print_article_content(output)
            await deal_article(spider, output)
            continue
        elif aten_cmd[0] == 'question':
            question_ids = [d.get('question').get('id') for d in aten_articles]
            if len(aten_cmd) != 2:
                print_colour('输入有误!', 'red')
                continue
            if aten_cmd[1] not in question_ids:
                print_colour('输入id有误!', 'red')
                continue
            assert len(ids) == len(question_ids)
            id_map = dict(zip(question_ids, ids))
            uid = id_map[aten_cmd[1]]
            await deal_question(spider, aten_cmd[1], uid)
            continue
        elif aten_cmd[0] == 'back':
            break
        else:
            print_colour('输入有误!', 'red')
            continue

# async def deal_fav(spider, url_token):
#     is_next = False
#     is_print = True
#     paging = {}
#     while True:
#         if is_print:
#             if is_next:
#                 next_url = paging['next']
#                 fav_list = await spider.get_fav_list(url_token, next_url)
#                 fid = fav_list['id']
#                 paging = fav_list.pop(-1)
#                 print_fav_list(fav_list)
#             else:
#                 fav_list = await spider.get_fav_list(url_token)
#                 paging = fav_list.pop(-1)
#                 print_fav_list(fav_list)
#             is_print = False
#             is_next = False
#         print_colour('', 'yellow')
#         remd_cmd = input(help_fav()).lower()
#         remd_cmd = remd_cmd.split(':')
#         if not remd_cmd:
#             print_colour('输入有误!', 'red')
#             continue
#         await app_exit(remd_cmd[0], spider)
#         if remd_cmd[0] == 'r':
#             print_fav_list(fav_list)
#             continue
#         elif remd_cmd[0] == "item":
#             await deal_items(spider,fid)
#             continue
#         elif remd_cmd[0] == 'n':
#             if paging.get('is_end'):
#                 print_colour('已是第一页!', 'red')
#                 continue
#             is_print = True
#             is_next = True
#             continue
#         elif remd_cmd[0] == 'back':
#             break
#         else:
#             print_colour('输入有误!', 'red')
#             continue


async def deal_items(spider,fid='114929484'):
    """
    处理推荐文章命令
    :param spider:
    :return:
    """
    is_next = False
    is_print = True
    paging = {}
    while True:
        if is_print:
            if is_next:
                next_url = paging['next']
                aten_articles = await spider.get_items_article(fid, next_url)
                paging = aten_articles.pop(-1)
                ids = [d.get('id') for d in aten_articles]
                print_items_article(aten_articles)
            else:
                aten_articles = await spider.get_items_article(fid)
                paging = aten_articles.pop(-1)
                ids = [d.get('id') for d in aten_articles]
                print_items_article(aten_articles)
            is_print = False
            is_next = False
        print_colour('', 'yellow')
        aten_cmd = input(help_item()).lower()
        aten_cmd = aten_cmd.split(':')
        if not aten_cmd:
            print_colour('输入有误!', 'red')
            continue
        await app_exit(aten_cmd[0], spider)
        if aten_cmd[0] == 'f':
            is_print = True
            continue
        elif aten_cmd[0] == 'r':
            print_items_article(aten_articles)
            continue
        elif aten_cmd[0] == 'n':
            if paging.get('is_end'):
                print_colour('已是第一页!', 'red')
                continue
            is_print = True
            is_next = True
            continue
        elif aten_cmd[0] == 'user':
            user_info = await spider.get_user_info(aten_cmd[1])
            if user_info == False:
                print_colour('用户不存在或url_token输入有误!', 'red')
                continue
            await deal_user(spider, aten_cmd[1])
            continue
        elif aten_cmd[0] == 'read':
            if len(aten_cmd) != 2:
                print_colour('输入有误!', 'red')
                continue
            if aten_cmd[1] not in ids:
                print_colour('输入id有误! 请检查id是否在此页', 'red')
                continue
            output = [d for d in aten_articles if d['id'] == aten_cmd[1]][0]
            print_article_content(output)
            await deal_article(spider, output)
            continue
        elif aten_cmd[0] == 'question':
            question_ids = [d.get('question').get('id') for d in aten_articles]
            if len(aten_cmd) != 2:
                print_colour('输入有误!', 'red')
                continue
            if aten_cmd[1] not in question_ids:
                print_colour('输入id有误!', 'red')
                continue
            assert len(ids) == len(question_ids)
            id_map = dict(zip(question_ids, ids))
            uid = id_map[aten_cmd[1]]
            await deal_question(spider, aten_cmd[1], uid)
            continue
        elif aten_cmd[0] == 'back':
            break
        else:
            print_colour('输入有误!', 'red')
            continue
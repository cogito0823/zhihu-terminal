import os
import html2text
from setting import SAVE_DIR

from typing import Any
"""
前景色	背景色	颜色
30	40	黑色
31	41	红色
32	42	绿色
33	43	黃色
34	44	蓝色(有问题)
35	45	紫红色
36	46	青蓝色
37	47	白色

显示方式	意义
0	终端默认设置
1	高亮显示
4	使用下划线
5	闪烁
7	反白显示
8	不可见
"""
colour_map = {
    'black': '30',
    'red': '31',
    'green': '32',
    'yellow': '33',
    'blue': '34',
    'purple': '35',
    'ultramarine': '36',
    'white': '37',
}

def print_colour(s: Any, colour: str='green', way: int=0, **kwargs):
    """打印颜色"""
    print(f'\033[{way};{colour_map[colour]};m{s}', **kwargs)

def print_logo():
    os.system("clear")
    logo = '''
                                                                                             ;$$;
                                                                                        #############
                                                                                   #############;#####o
                                                          ##                 o#########################
                                                          #####         $###############################
                                                          ##  ###$ ######!    ##########################
                               ##                        ###    $###          ################### ######
                               ###                      ###                   ##o#######################
                              ######                  ;###                    #### #####################
                              ##  ###             ######                       ######&&################
                              ##    ###      ######                            ## ############ #######
                             o##      ########                                  ## ##################
                             ##o                ###                             #### #######o#######
                             ##               ######                             ###########&#####
                             ##                ####                               #############!
                            ###                                                     #########
                   #####&   ##                                                      o####
                 ######     ##                                                   ####*
                      ##   !##                                               #####
                       ##  ##*                                            ####; ##
                        #####                                          #####o   #####
                         ####                                        ### ###   $###o
                          ###                                            ## ####! $###
                          ##                                            #####
                          ##                                            ##
                         ;##                                           ###                           ;
                         ##$                                           ##
                    #######                                            ##
                #####   &##                                            ##
              ###       ###                                           ###
             ###      ###                                             ##
             ##     ;##                                               ##
             ##    ###                                                ##
              ### ###                                                 ##
                ####                                                  ##
                 ###                                                  ##
                 ##;                                                  ##
                 ##$                                                 ##&
                  ##                                                 ##
                  ##;                                               ##
                   ##                                              ##;
                    ###                                          ###         ##$
                      ###                                      ###           ##
       ######################                              #####&&&&&&&&&&&&###
     ###        $#####$     ############&$o$&################################
     #                               $&########&o
    '''
    print_colour(logo, 'ultramarine')

# ========================= 用户 =============================

def print_user_info(user_info: dict):
    d = user_info
    
    gender = d.get('gender')
    if gender == -1:
        gender = ''
    elif gender == 0:
        gender = '女'
    elif gender == 1:
        gender = '男'
        
    print_colour('=' * 60, 'white')
    print_colour(f"{d.get('name')}", 'purple')
    print_colour(f"性别：{gender}", 'purple')
    print_colour(f"(签名：{d.get('headline')})", 'purple')
    print_colour(f"(简介：{d.get('description')})", 'purple')
    print_colour(f"回答：{d.get('question_count')}", 'purple')
    print_colour(f"文章：{d.get('articles_count')}", 'purple')
    print_colour(f"收藏夹：{d.get('favorite_count')}", 'purple')
    print_colour(f"被收藏：{d.get('favorited_count')}", 'purple')
    print_colour(f"被赞同{d.get('voteup_count')}次", 'purple')
    print_colour(f"被感谢{d.get('thanked_count')}次", 'purple')
    
    badges = d.get('badge')
    educations = d.get('educations')
    employments = d.get('employments')
    business = d.get('business')
    print_colour('徽章: ')
    if badges:
        for badge in badges:
            print_colour(f"    {badge.get('type')}: {badge.get('description')}", 'purple')
        
    print_colour('教育经历: ')
    if educations:
        for education in educations:
            if education.get('school'):
                if education.get('major'):
                    print_colour(f"    {education.get('school').get('name')}·{education.get('major').get('name')}", 'purple')
                else:
                    print_colour(f"    {education.get('school').get('name')}", 'purple')
            elif education.get('major'):
                print_colour(f"    {education.get('major').get('name')}", 'purple')
    
    if business:        
        print_colour(f"所在行业：{business.get('name')}", 'purple')
    
    print_colour('职业经历: ')
    if employments:
        for employment in employments:
            if employment.get('company'):
                if employment.get('job'):
                    print_colour(f"    {employment.get('company').get('name')} [{employment.get('job').get('name')}]", 'purple')
                else:
                    print_colour(f"    {employment.get('company').get('name')}",'purple')
            elif employment.get('job'):
                print_colour(f"    [{employment.get('job').get('name')}]",'purple')
    
    fav_list = d.get('data')
    if fav_list:
        for item in fav_list:
            print_colour('=' * 60, 'white')
            print_colour(f'article_id:{item["id"]}', 'purple')
            print_colour(f'question_id:{item["question"]["id"]}', 'purple')
            print_colour(item['question']['title'], 'purple', end='')
            print_colour(f"({item['author']['name']} uid:{item['author'].get('url_token')})", 'purple')
            print_colour(item['excerpt'])
            print_colour(f"*赞同数{item.get('voteup_count')} 评论数{item.get('comment_count')}", 'purple')
# ========================= 展示页  ==========================

def print_recommend_article(output: list):
    """
    打印推荐文章简述
    :param output:
    :return:
    """
    for d in output:
        print_colour('=' * 60, 'white')
        print_colour(f"{d['type']}: {d['question']['title']}", 'purple', end='')
        print_colour(f"({d['author']['name']} uid:{d['author'].get('url_token')})", 'purple')
        print_colour(f"赞同数{d.get('voteup_count')} 感谢数{d.get('thanks_count', 0)} "
                     f"评论数{d.get('comment_count')} 浏览数{d.get('visited_count')}", 'purple')
        print_colour(d['excerpt'])
        print_colour(f'article_id:{d["id"]} question_id:{d["question"]["id"]}', 'purple')
        
        
def print_aten_article(output: list):
    """
    打印关注文章简述
    :param output:
    :return:
    """
    for d in output:
        print_colour('=' * 60, 'white')
        actorss = []
        for j in d['actors']:
            if j.get('name'):
                actorss.append(j.get('name'))
        action_text_tpl = d['action_text_tpl'][2:]
        print_colour(f'{actorss} {action_text_tpl}', 'purple')
        print_colour(f'article_id:{d["id"]}', 'purple')
        print_colour(f'question_id:{d["question"]["id"]}', 'purple')
        print_colour(d['question']['title'], 'purple', end='')
        print_colour(f"({d['author']['name']} uid:{d['author'].get('url_token')})", 'purple')
        print_colour(d['excerpt'])
        print_colour(f"*赞同数{d.get('voteup_count')} 感谢数{d.get('thanks_count', 0)} "
                     f"评论数{d.get('comment_count')} 浏览数{d.get('visited_count')}*", 'purple')

def print_act_article(output: list):
    """
    打印关注文章简述
    :param output:
    :return:
    """
    for d in output:
        print_colour('=' * 60, 'white')
        action_text_tpl = d['action_text_tpl']
        print_colour(f'{action_text_tpl}', 'purple')
        print_colour(f'article_id:{d["id"]}', 'purple')
        print_colour(f'question_id:{d["question"]["id"]}', 'purple')
        print_colour(d['question']['title'], 'purple', end='')
        print_colour(f"({d['author']['name']} uid:{d['author'].get('url_token')})", 'purple')
        print_colour(d['excerpt'])
        print_colour(f"*赞同数{d.get('voteup_count')} 感谢数{d.get('thanks_count', 0)} "
                     f"评论数{d.get('comment_count')} 浏览数{d.get('visited_count')}*", 'purple')

def print_fav_list(output: list):
    for d in output:
        print_colour('=' * 60, 'white')
        print_colour(f'fav_list_id:{d["id"]}', 'purple')
        print_colour(f"{d['title']} 文章数：d['answer_count']", 'purple', end='')
        print_colour(f"({d['creator']['name']} uid:{d['creator'].get('url_token')})", 'purple')
        print_colour(d['description'])
        print_colour(f"*关注数{d.get('follower_count')} 评论数{d.get('comment_count')}\n", 'purple')
        
def print_items_article(output):
    for d in output:
        print_colour('=' * 60, 'white')
        print_colour(f'article_id:{d["id"]}', 'purple')
        print_colour(f'question_id:{d["question"]["id"]}', 'purple')
        print_colour(d['question']['title'], 'purple', end='')
        print_colour(f"({d['author']['name']} uid:{d['author'].get('url_token')})", 'purple')
        print_colour(d['excerpt'])
        print_colour(f"*赞同数{d.get('voteup_count')} 评论数{d.get('comment_count')}", 'purple')

# ========================= 文章  =============================

def print_article_content(output: dict):
    """
    打印文章内容
    :param output:
    :return:
    """
    content = output['content']
    title = output['question']['title']
    question_id = output['question']['id']
    article_id = output["id"]
    typ = output['type']
    if typ == 'zvideo':
        url = f'https://www.zhihu.com/zvideo/{article_id}'
    elif article_id and not question_id:
        url = f'https://zhuanlan.zhihu.com/p/{article_id}'
    else:
        url = f'https://www.zhihu.com/question/{question_id}/answer/{article_id}'
    content = html2text.html2text(content)
    print_colour('-----------------------------------------------------', 'purple')
    print_colour(f'|article_id:{article_id}', 'purple')
    print_colour(f'|question_id:{question_id}', 'purple')
    print_colour(f'|title:{title}', 'purple')
    print_colour(f'|原文链接:{url}', 'purple')
    print_colour('-----------------------------------------------------', 'purple')
    print_colour(content)
    
# ========================= 问题页  =============================

def print_question(question: dict):
    """
    打印问题及第默认排序下的第一个回答
    :param output:
    :return:
    """
    title = question['title']
    # question_id = question['id']
    question_content = question['detail']
    question_content = html2text.html2text(question_content)
    print_colour('*' * 50, 'purple')
    print_colour(f'标题:{title}')
    print_colour('问题详情:')
    print_colour(question_content)
    print_colour('*' * 50, 'purple')

# ========================= 评论页  =============================

def print_comments(output: list):
    """
    打印评论
    :param output:
    :return:
    """
    for d in output:
        author = d.get('author').get('name')
        reply_to_author = d.get('reply_to_author').get('name')
        content = d.get('content')
        vote_count = d.get('vote_count')
        comment_id = d.get('id')
        child_comments = d.get('child_comments')
        print_colour(f'comment_id:{comment_id}', 'purple')
        if d.get('featured'):
            print_colour('热评🔥', end='')
        if reply_to_author:
            print_colour(f'{author}->{reply_to_author}', end='')
        else:
            print_colour(f'{author}', end='')
        print_colour(f'(赞:{vote_count}):{content}')
        if child_comments:
            for clild in child_comments:
                author = clild.get('author').get('name')
                reply_to_author = clild.get('reply_to_author').get('name')
                content = clild.get('content')
                vote_count = clild.get('vote_count')
                comment_id = clild.get('id')
                print_colour(f'         comment_id:{comment_id}', 'purple')
                if d.get('featured'):
                    print_colour('         热评🔥', end='')
                if reply_to_author:
                    print_colour(f'         {author}->{reply_to_author}', end='')
                else:
                    print_colour(f'         {author}', end='')
                print_colour(f'         (赞:{vote_count}):{content}')
                print_colour('         *********************************************************', 'blue')
        print_colour('==========================================================', 'blue')

# ========================== 互动  =============================

def print_vote_thank(output: dict, typ: str):
    """
    打印赞同感谢  up', 'down', 'neutral'
    :param output:
    :return:
    """
    if output.get('error'):
        print_colour(output.get('error'), 'red')
    elif typ == 'thank':
        print_colour(f'感谢成功!感谢总数{output["thanks_count"]}')
    elif typ == 'unthank':
        print_colour(f'取消感谢!感谢总数{output["thanks_count"]}')
    elif typ == 'up':
        print_colour(f'赞同成功!赞同总数{output["voteup_count"]}')
    elif typ == 'down':
        print_colour(f'反对成功!赞同总数{output["voteup_count"]}')
    else:
        print_colour(f'保持中立!赞同总数{output["voteup_count"]}')

def print_vote_comments(output: dict, typ: str):
    """
    打印赞同感谢  up', 'down', 'neutral'
    :param output:
    :return:
    """
    if output.get('error'):
        print_colour(output.get('error'), 'red')
    elif typ == 'up':
        print_colour(f'点赞评论成功!被赞总数{output["vote_count"]}')
    elif typ == 'neutral':
        print_colour(f'保持中立!被赞总数{output["vote_count"]}')

def print_save(article: dict):
    """
    保存文章到本地
    :param article:
    :return:
    """
    uid = article.get('id')
    title = article.get('question').get('title')
    content = article.get('content')
    save_dir = SAVE_DIR or '/tmp/zhihu_save'
    file = f'{save_dir}/{title}_{uid}.html'
    with open(file, 'w') as f:
        head = '<head> <meta charset="utf-8"><meta http-equiv="Content-Type"' \
               ' content="text/html; charset=utf-8" /> </head>'
        f.write(head)
        f.write(content)
    print_colour(f'保存成功!-->{file}')

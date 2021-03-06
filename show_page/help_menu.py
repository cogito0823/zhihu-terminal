#!/usr/bin/env python3
# -*- encoding: utf-8 -*-

'''
@File    :   help_menu.py
@Time    :   2020/05/12 15:58:21
@Author  :   cogito0823
@Contact :   754032908@qq.com
@Desc    :   菜单模板
'''

# 主菜单
def help_main():
    output = "\n主菜单\n" \
           "**********************************************************\n" \
           "**  remd:                    查看推荐内容\n" \
           "**  aten:                    查看关注内容\n" \
           "**  fav:                     查看收藏夹\n" \
           "**  item:                    查看收藏内容\n" \
           "**  q:                       退出系统\n" \
           "**********************************************************\n"
    return output

# 推荐页菜单
def help_recommend():
    output = "\n推荐页菜单\n" \
           "**********************************************************\n" \
           "**  f:                       刷新推荐内容\n" \
           "**  r:                       再次显示本层内容\n" \
           "**  user:uid                 查看用户\n" \
           "**  read:article_id          查看文章具体内容(进入下一级菜单)\n" \
           "**  question:question_id     查看问题下的其他回答(进入下一级菜单)\n" \
           "**  back:                    返回上层\n" \
           "**  q:                       退出系统\n" \
           "**********************************************************\n"
    return output

# 关注页菜单
def help_aten():
    output = "\n关注页菜单\n" \
           "**********************************************************\n" \
           "**  f:                       刷新动态内容\n" \
           "**  r:                       再次显示本层内容\n" \
           "**  n:                       下一页\n" \
           "**  user:uid                 查看用户\n" \
           "**  read:article_id          查看文章具体内容(进入下一级菜单)\n" \
           "**  question:question_id     查看问题下的其他回答(进入下一级菜单)\n" \
           "**  back:                    返回上层\n" \
           "**  q:                       退出系统\n" \
           "**********************************************************\n"
    return output

# 动态页菜单
def help_act():
    output = "\n动态页菜单\n" \
           "**********************************************************\n" \
           "**  f:                       刷新关注内容\n" \
           "**  r:                       再次显示本层内容\n" \
           "**  n:                       下一页\n" \
           "**  user:uid                 查看用户\n" \
           "**  read:article_id          查看文章具体内容(进入下一级菜单)\n" \
           "**  question:question_id     查看问题下的其他回答(进入下一级菜单)\n" \
           "**  back:                    返回上层\n" \
           "**  q:                       退出系统\n" \
           "**********************************************************\n"
    return output

# 收藏页菜单
def help_item():
    output = "\n收藏页菜单\n" \
           "**********************************************************\n" \
           "**  f:                       刷新收藏内容\n" \
           "**  r:                       再次显示本层内容\n" \
           "**  n:                       下一页\n" \
           "**  user:uid                 查看用户\n" \
           "**  read:article_id          查看文章具体内容(进入下一级菜单)\n" \
           "**  question:question_id     查看问题下的其他回答(进入下一级菜单)\n" \
           "**  back:                    返回上层\n" \
           "**  q:                       退出系统\n" \
           "**********************************************************\n"
    return output

# 文章页菜单
def help_article():
    output = "\n文章页菜单\n" \
            "**********************************************************\n" \
            "**  r                       再次显示本层内容\n" \
            "**  back                    返回上层\n" \
            "**  q                       退出系统\n" \
            "**  save                    保存到本地\n" \
            "**  enshrine                收藏回答\n" \
            "**  question                查看问题下的其他回答\n" \
            "**  up                      赞同\n" \
            "**  down                    反对\n" \
            "**  neutral                 中立,可以取消对回答的赞同或反对\n" \
            "**  thank                   感谢\n" \
            "**  unthank                 取消感谢\n"\
            "**  comment                 查看评论(查看评论, 回复评论等将进入下一级菜单)\n"\
            "**********************************************************\n"
    return output

# 评论页菜单
def help_comments():
    output = "\n评论页菜单\n" \
            "**********************************************************\n" \
            "**  back                    返回上层\n" \
            "**  r                       再次显示本层内容\n" \
            "**  q                       退出系统\n" \
            "**  n                       显示下一页\n" \
            "**  p                       显示上一页\n" \
            "**  com:comment_id          回复评论,点赞等功能(进入下级菜单)\n" \
            "**********************************************************\n"
    return output

# 评论页菜单2
def help_comments2():
    output = "\n评论页菜单2\n" \
            "**********************************************************\n" \
            "**  back                    返回上层\n" \
            "**  q                       退出系统\n" \
            "**  up                      点赞\n" \
            "**  neutral                 中立,可以取消对点赞\n" \
            "**  reply:content           回复评论\n" \
            "**********************************************************\n"
    return output

# 问题页菜单
def help_question():
    output = "\n问题页菜单\n" \
            "**********************************************************\n" \
            "**  qsdl                    查看问题详情\n" \
            "**  read:article_id         查看回答具体内容(进入下一级菜单)\n" \
            "**  user:uid                查看用户\n" \
            "**  n                       显示下一页\n" \
            "**  p                       显示上一页\n" \
            "**  r                       再次显示本层内容\n" \
            "**  back                    返回上层\n" \
            "**  q                       退出系统\n" \
            "**********************************************************\n"
    return output

# 用户页菜单
def help_user():
    output = "\n用户页菜单\n" \
            "**********************************************************\n" \
            "**  back                    返回上层\n" \
            "**  q                       退出系统\n" \
            "**  act                     查看动态\n" \
            "**  fav:                    查看收藏夹\n" \
            "**  col:                    查看专栏\n" \
            "**  r                       再次显示本层内容\n" \
            "**********************************************************\n"
    return output

def help_fav():
    output = "\n用户页菜单\n" \
            "**********************************************************\n" \
            "**  back                    返回上层\n" \
            "**  q                       退出系统\n" \
            "**  act                     查看动态\n" \
            "**  fav:fid                 查看收藏夹\n" \
            "**  col:col_id              查看专栏\n" \
            "**  r                       再次显示本层内容\n" \
            "**********************************************************\n"
    return output
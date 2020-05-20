import os
import sys
import asyncio
from aiohttp import ClientTimeout
from zhihu_client import ZhihuClient
from data_extractor import DataExtractor

from utils import print_colour
from utils import get_com_func
from aiohttp import TCPConnector

from setting import USER as default_username
from setting import PASSWORD as default_password
from setting import SAVE_DIR
from setting import COOKIE_FILE,proxy
from utils import print_colour
from print_beautify import print_logo
from help_menu import help_main
from deal_action import RemdPage
from deal_action import AtenPage
from deal_action import deal_user
from deal_action import deal_items
from deal_action import app_exit
       
async def loading():
    await asyncio.sleep(2)
    print_colour(f'\n正在加载中...\n', 'ultramarine') 
    
async def run(client):
    spider = DataExtractor(client)
    self_info = await spider.get_self_info()
    print_colour(f'hello {self_info["name"]} 欢迎使用知乎~', 'ultramarine')
    
    remdPage, atenPage, load = await asyncio.gather(RemdPage.create(spider),AtenPage.create(spider),loading())
    flag = True
    while flag:
        print_colour('', 'yellow')
        cmd = input(help_main()).lower()
        if not cmd:
            print_colour('输入有误!', 'red')
            continue
        await app_exit(cmd, spider) 
        if cmd == 'remd':
            await remdPage.deal_remd(spider)
        elif cmd == 'aten':
            await atenPage.deal_aten(spider)
        elif cmd == 'item':
            await deal_items(spider)
        elif cmd == 'fav':
            await spider.get_fav_list()
        else:
            print_colour('输入有误!', 'red')
            continue


def check_setting():
    save_dir = SAVE_DIR or '/tmp/zhihu_save'
    if not os.path.exists(save_dir):
        os.makedirs(save_dir)


async def login(user='', password='', whether_load_cookies = True):
    client = ZhihuClient(user, password, connector=TCPConnector(ssl=False))
    load_cookies = False
    if whether_load_cookies and os.path.exists(client.cookie_file):
        # 如果cookie缓存存在优先读取缓存
        load_cookies = True
    is_suc = await client.login(load_cookies=load_cookies)
    if is_suc == 'relogin':
        await client.close()
        return False
    return client

async def get_zhihu_client():
    check_setting()
    print("你可以在任何时刻输入'back'返回上一层，或输入'q'退出程序。")
    await asyncio.sleep(1)
    while True:
        use_cookies = input("是否直接使用cookies登录(y|n): ")
        await app_exit(use_cookies)
        if use_cookies == 'n':
            while True:
                use_default_account = input('是否使用默认账号(y|n): ')
                await app_exit(use_default_account)
                if use_default_account == 'y':
                    USER = default_username
                    PASSWORD = default_password
                    client =  await login(USER, PASSWORD, False)
                    if not client:
                        continue
                    else:
                        return client
                elif use_default_account == 'back':
                    break
                elif use_default_account == 'n':
                    while True:
                        USER = input('请输入手机号: ')
                        await app_exit(USER)
                        if USER == 'back':
                            break
                        while True:
                            PASSWORD = input('请输入密码: ')
                            await app_exit(PASSWORD)
                            if PASSWORD == 'back':
                                break
                            client =  await login(USER, PASSWORD, False)
                            if not client:
                                continue
                            else:
                                return client
                else:
                    print('输入有误！')
                    continue
        elif use_cookies == 'y':
            client =  await login()
            if not client:
                continue
            else:
                return client
        else:
            print('输入有误！')
            continue

async def main():
    try:
        zhihu_client = False
        zhihu_client = await get_zhihu_client()
        print_logo()
        await run(zhihu_client)
    finally:
        print_colour('欢迎再次使用')
        if zhihu_client:
            await zhihu_client.close()


if __name__ == '__main__':
    asyncio.run(main())
    

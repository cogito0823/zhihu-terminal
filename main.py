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
from deal_action import deal_remd
from deal_action import deal_aten

async def app_exit(cmd: str, spider):
    if cmd in('q', 'quit', 'exit'):
        await spider.client.close()
        os._exit(0)
        
async def run(client):
    spider = DataExtractor(client)
    self_info = await spider.get_self_info()
    print_colour(f'hello {self_info["name"]} 欢迎使用知乎~', 'ultramarine')
    flag = True
    while flag:
        print_colour('', 'yellow')
        cmd = input(help_main()).lower()
        if not cmd:
            print_colour('输入有误!', 'red')
            continue
        await app_exit(cmd, spider)
        if cmd == 'remd':
            await deal_remd(spider)
        elif cmd == 'aten':
            await deal_aten(spider)
        else:
            print_colour('输入有误!', 'red')
            continue


def check_setting():
    save_dir = SAVE_DIR or '/tmp/zhihu_save'
    if not os.path.exists(save_dir):
        os.makedirs(save_dir)


async def login(user='', password='', whether_load_cookies = True):
    """
    登录
    :param user:
    :param password:
    :return:
    """
    client = ZhihuClient(user, password, connector=TCPConnector(ssl=False))
    load_cookies = False
    if whether_load_cookies and os.path.exists(client.cookie_file):
        # 如果cookie缓存存在优先读取缓存
        load_cookies = True
    await client.login(load_cookies=load_cookies)
    return client


async def main():
    try:
        while True:
            check_setting()
            use_cookies = input("是否直接使用cookies登录(y|n): ")
            if use_cookies == 'n':
                use_default_account = input('是否使用默认账号(y|n): ')
                if use_default_account == 'y':
                    USER = default_username
                    PASSWORD = default_password
                elif use_default_account == 'n':
                    USER = input('请输入手机号(输入"back"可以返回上级选择)：')
                    if USER == 'back':
                        continue
                    PASSWORD = input('请输入密码')
                else:
                    print('输入有误！')
                    continue
                client = await login(USER, PASSWORD, False)
            elif use_cookies == 'y':
                client = await login(True)
            else:
                print('输入有误！')
                continue
            print_logo()
            await run(client)
            break
    # except Exception as e:
    #     print_colour(e, 'red')
    finally:
        print_colour('欢迎再次使用')
        await asyncio.sleep(0)
        await client.close()


if __name__ == '__main__':
    # asyncio.run(main())
    asyncio.get_event_loop().run_until_complete(main())

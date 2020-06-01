"""
保存有知乎登录cookie的ClientSession
"""
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
from show_page.print_beautify import print_colour
from log import get_logger
from setting import COOKIE_FILE,proxy
from setting import proxy_headers
from client_login import detect_captcha
from aiohttp import TCPConnector
from deal_action import app_exit

class ZhihuClient(aiohttp.ClientSession):
    """扩展ClientSession"""

    def __init__(self, user='', password='', *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.user = user
        self.password = password
        headers = {
            'Host': 'www.zhihu.com',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.103 Safari/537.36',
            #'Connection': 'Keep-Alive',
            'Referer': 'https://www.zhihu.com/',
            #'x-zse-83': '3_2.0',
            'accept-encoding': 'gzip, deflate'
        }
        headers.update(proxy_headers)
        self._default_headers = headers
        self.logger = get_logger()
        self.cookie_file = COOKIE_FILE or '/tmp/cookies.pick'

    async def login(self, load_cookies: bool=False) -> None:
        """
        登录
        :param load_cookies: 是否加载cookie
        :return:
        """
        if load_cookies:
            self.cookie_jar.load(self.cookie_file)
            self.logger.debug(f'加载cookies从:{self.cookie_file}')
            is_succ = await self.check_login()
            if is_succ:
                print_colour('登录成功!', colour='green')
                return
            else:
                print_colour('通过缓存登录失败尝试重新登录', 'red')
                self.cookie_jar.clear()
                os.remove(self.cookie_file)

        login_data = {
            'client_id': 'c3cef7c66a1843f8b3a9e6a1e3160e20',
            'grant_type': 'password',
            'source': 'com.zhihu.web',
            'username': self.user,
            'password': self.password,
            'lang': 'en',  # en 4位验证码, cn 中文验证码
            'ref_source': 'other_https://www.zhihu.com/signin?next=%2F',
            'utm_source': ''
        }
        xsrf = await self._get_xsrf()
        headers = {
                'accept-encoding': 'gzip, deflate, br',
                'Host': 'www.zhihu.com',
                'Referer': 'https://www.zhihu.com/',
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.103 Safari/537.36',
                'content-type': 'application/x-www-form-urlencoded',
                'x-zse-83': '3_2.0',
                'x-xsrftoken': xsrf
            }
        headers.update(proxy_headers)
        # 获取验证码后登录，验证码错误则重新登录
        while True:
            captcha = await self._get_captcha()
            if not captcha:
                continue
            if captcha == '0':
                captcha = ''
            elif captcha == 'back':
                return 'relogin'
            timestamp = int(time.time() * 1000)
            login_data.update({
                'captcha': captcha,
                'timestamp': timestamp,
                'signature': self._get_signature(timestamp, login_data)
            })
            data = self._encrypt(login_data)
            url = 'https://www.zhihu.com/api/v3/oauth/sign_in'
            async with self.post(url, data=data, headers=headers, proxy=proxy) as r:
                resp = await r.text()
                if 'error' in resp:
                    print_colour(json.loads(resp)['error'], 'red')
                    self.logger.debug(f"登录失败:{json.loads(resp)['error']}")
                    code = json.loads(resp)['error']['code']
                    if not code == 120005:
                        return 'relogin'
                    else:
                        continue
                self.logger.debug(resp)
                is_succ = await self.check_login()
                if is_succ:
                    print_colour('登录成功!', colour='green')
                    return
                else:
                    print_colour('登录失败!', colour='red')
                    sys.exit()

    async def _get_captcha(self) -> str:
        """
        请求验证码的 API 接口，无论是否需要验证码都需要请求一次
        如果需要验证码会返回图片的 base64 编码
        根据 lang 参数匹配验证码，需要人工输入
        :param lang: 返回验证码的语言(en/cn)
        :return: 验证码的 POST 参数
        """

        url = 'https://www.zhihu.com/api/v3/oauth/captcha?lang=en'
        async with self.get(url, proxy=proxy) as r:
            resp = await r.text()
            show_captcha = re.search(r'true', resp)
        if show_captcha:
            while True:
                async with self.put(url, proxy=proxy) as r:
                    resp = await r.text()
                json_data = json.loads(resp)
                img_base64 = json_data['img_base64'].replace(r'\n', '')
                with open(f'./captcha.jpg', 'wb') as f:
                    f.write(base64.b64decode(img_base64))
                whether_use_detect_aptcha =input('是否使用打码平台(y|n)(输入"back"可上一级): ')
                if whether_use_detect_aptcha == 'back':
                    return 'back'
                await asyncio.sleep(0.3)
                await app_exit(whether_use_detect_aptcha)
                # 识别验证码
                if whether_use_detect_aptcha == 'y':
                        pic_str = detect_captcha.detect('captcha.jpg')
                        capt = pic_str
                elif whether_use_detect_aptcha == 'n':
                    capt = input('请输入图片里的验证码：')
                    await app_exit(capt)
                    if capt == 'back':
                        continue
                else:
                    print('输入错误')
                    continue
                # 这里必须先把参数 POST 验证码接口
                await self.post(url, data={'input_text': capt}, proxy=proxy)
                return capt
        return '0'

    async def check_login(self) -> bool:
        """
        检查登录状态，访问登录页面出现跳转则是已登录，
        如登录成功保存当前 Cookies
        :return: bool
        """
        url = 'https://www.zhihu.com/'
        async with self.get(url, allow_redirects=False, proxy=proxy) as r:
            if r.status == 200:
                self.cookie_jar.save(self.cookie_file)
                self.logger.debug(f'保存cookies到->{self.cookie_file}')
                return True
            else:
                self.logger.debug(await r.text())
                self.logger.debug(r.headers)
                self.logger.debug(r.status)
            return False

    async def _get_xsrf(self) -> str:
        """
        从登录页面获取 xsrf
        :return: str
        """
        async with self.get('https://www.zhihu.com/', allow_redirects=False, proxy=proxy) as r:
            self.logger.debug('尝试获取xsrf token')
            if r.cookies.get('_xsrf'):
                self.logger.debug(f'获取成功{r.cookies.get("_xsrf").value}')
                return r.cookies.get('_xsrf').value
        raise AssertionError('获取 xsrf 失败')

    def _get_signature(self, timestamp: Union[int, str], login_data: dict) -> str:
        """
        通过 Hmac 算法计算返回签名
        实际是几个固定字符串加时间戳
        :param timestamp: 时间戳
        :return: 签名
        """
        ha = hmac.new(b'd1b964811afb40118a12068ff74a12f4', digestmod=hashlib.sha1)
        grant_type = login_data['grant_type']
        client_id = login_data['client_id']
        source = login_data['source']
        ha.update(bytes((grant_type + client_id + source + str(timestamp)), 'utf-8'))
        return ha.hexdigest()

    @staticmethod
    def _encrypt(form_data: dict) -> str:
        with open(f'./client_login/encrypt.js') as f:
            js = execjs.compile(f.read())
            return js.call('b', urlencode(form_data))


if __name__ == '__main__':
    from setting import USER, PASSWORD

    async def test():
        client = ZhihuClient(user=USER, password='ddfgdfgr345434', connector=TCPConnector(ssl=False))
        await client.login(load_cookies=False)
        await client.close()
    asyncio.run(test())
    
    
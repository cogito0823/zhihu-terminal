"""
路径使用绝对路径
"""
DEBUG = False

User_Agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.113 Safari/537.36'

headers = {
            'Host': 'www.zhihu.com',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 '
                          '(KHTML, like Gecko) Chrome/66.0.3359.181 Safari/537.36',
            #'Connection': 'Keep-Alive',
            'Referer': 'https://www.zhihu.com/',
            'accept-encoding': 'gzip, deflate'
        }
LOG_DIR = '/tmp/zhihu'  # df: /tmp/zhihu  debug模式下存放日志

COOKIE_FILE = '/tmp/cookies.pick'  # df: /tmp/cookies.pick   缓存的cookie文件

SAVE_DIR = '/tmp/zhihu_save'  # df: /tmp/zhihu_save   保存回答到本地

# USER = '13315728454'  # 必填  账号
USER = '13686005254'
# PASSWORD = 'shenzhenmao18'   # 必填  密码
PASSWORD = 'asd745699887'
# 超级鹰
CJY_PASSWORD = 'b4zPfH5rCeM7c3D'

CJY_SOFT_ID = '904588'

CJY_USER = 'cogito'

# '您预装的是 Linux 操作系统, 请您请稍等 10分钟 后用SSH连接您的云服务器
# 服务器名：cogito
# 远程连接：123.52.202.148
# SSH端口：20016
# 用户名：root
# 机器密码：eessYsC9jqqG
# 宽带账户：639324333664
# 宽带密码：321321'
# 171.13.250.153:3128

#proxy = 'http://171.8.249.136:3128'

#########################################################################

ip_port = 'secondtransfer.moguproxy.com:9001'

proxy = "http://" + ip_port

appKey =  'ZnZiajc3Q01zNU1WM1lRMTpBdWFSSDRPYnF6TmRKM1ZF'

proxy_headers = {"Proxy-Authorization": 'Basic ZnZiajc3Q01zNU1WM1lRMTpBdWFSSDRPYnF6TmRKM1ZF'}

#########################################################################

# from ss import auth

# proxy = 'http://forward.xdaili.cn:80'

# proxy_headers = {"Proxy-Authorization": auth}
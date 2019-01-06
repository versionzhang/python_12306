import requests

from global_data.useragent import CHROME_USER_AGENT

LOGIN_SESSION = requests.session()

# check left ticket doesn't need login.
NOTLOGIN_SESSION = requests.session()


LOGIN_SESSION.headers.update({
            'Host': r'kyfw.12306.cn',
            'Referer': 'https://kyfw.12306.cn/otn/login/init',
            'User-Agent': CHROME_USER_AGENT,
        })


NOTLOGIN_SESSION.headers.update({
            'Host': r'kyfw.12306.cn',
            'Referer': 'https://kyfw.12306.cn/otn/login/init',
            'User-Agent': CHROME_USER_AGENT,
        })

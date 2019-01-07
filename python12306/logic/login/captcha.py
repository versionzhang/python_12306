import base64
from io import BytesIO

from PIL import Image

import requests
from hashlib import md5

from global_data.session import LOGIN_SESSION
from global_data.url_conf import LOGIN_URLMAPPING
from global_data.useragent import CHROME_USER_AGENT

from config import Config
from utils.log import Log

from utils.net import send_requests, json_status, send_captcha_requests, get_captcha_image



class RClient(object):

    def __init__(self):
        self.username = Config.auto_code_account_ruokuai.user
        self.password = md5(Config.auto_code_account_ruokuai.pwd.encode()).hexdigest()
        self.soft_id = "119728"
        self.soft_key = "860e0eb28055431192d8dec771135ec8"
        self.base_params = {
            'username': self.username,
            'password': self.password,
            'softid': self.soft_id,
            'softkey': self.soft_key,
        }
        self.headers = {
            'Connection': 'Keep-Alive',
            'Host': 'api.ruokuai.com',
            'User-Agent': CHROME_USER_AGENT,
        }

    def rk_create(self, im_string, timeout=60):
        """
        im: 图片字节
        im_type: 题目类型
        """
        params = {
            'typeid': 6113,
            'timeout': timeout,
        }
        params.update(self.base_params)
        files = {'image': ('a.jpg', im_string)}
        r = requests.post('http://api.ruokuai.com/create.json', data=params, files=files, headers=self.headers)
        #
        Log.v("使用若快进行验证码识别")
        data = r.json()
        Log.v(data)
        return data


class NormalCaptchaUtil(object):
    success_code = '4'

    @staticmethod
    def getcaptcha():
        data = get_captcha_image(LOGIN_SESSION, LOGIN_URLMAPPING["normal"]["captcha"])
        img_binary = base64.b64decode(data["image"])
        return img_binary

    def check(self, results):
        params_data = {
            'answer': results,
            'rand': 'sjrand',
            'login_site': 'E'
        }
        json_response = send_captcha_requests(LOGIN_SESSION,
                                              LOGIN_URLMAPPING["normal"]["captchaCheck"],
                                              params=params_data)
        Log.v('normal login captcha verify: %s' % json_response)
        return json_status(json_response, [], ok_code=self.success_code)


class OtherCaptchaUtil(object):
    success_code = '1'

    @staticmethod
    def getcaptcha():
        data = get_captcha_image(LOGIN_SESSION, LOGIN_URLMAPPING["other"]["captcha"])
        img_binary = base64.b64decode(data["image"]).encode()
        return img_binary

    def check(self, results):
        form_data = {
            'randCode': results,
            'rand': 'sjrand',
        }

        json_response = send_requests(LOGIN_SESSION,
                                      LOGIN_URLMAPPING["other"]["captchaCheck"],
                                      data=form_data)
        Log.v('other login captcha verify: %s' % json_response)

        def verify(response):
            return response['status'] and self.success_code == response['data']['result']

        v = verify(json_response)
        return v, "Error" if not v else v, "ok"


class Captcha(object):
    captcha = {"normal": NormalCaptchaUtil(), "other": OtherCaptchaUtil()}
    results = ''

    def __init__(self, login_type, method='hand'):
        """

        :param login_type: normal
        :param method: hand (手动打码) ruokuai(若快打码)
        """
        self.login_type = login_type
        self.util = self.captcha[self.login_type]
        self.method = method

    def __getattribute__(self, item):
        if item in ("getcaptcha", "check"):
            return getattr(self.util, item)
        return object.__getattribute__(self, item)

    @staticmethod
    def trans_captcha_results(indexes, sep=r','):
        coordinates = ['40,40', '110,40', '180,40', '250,40', '40,110', '110,110', '180,110', '250,110']
        results = []
        for index in indexes.split(sep=sep):
            results.append(coordinates[int(index)])
        return ','.join(results)

    def generator_image(self):
        while True:
            data = self.getcaptcha()
            try:
                img = Image.open(BytesIO(data))
                img.close()
                break
            except OSError:
                Log.e("获取验证码图片失败, 重试获取")
                continue
        return data

    def verify(self):
        if Config.auto_code_enable and Config.auto_code_method == 'ruokuai':
            self.method = 'ruokuai'
        m = getattr(self, "verifyhandle_{method}".format(method=self.method))
        return m()

    def verifyhandle_ruokuai(self):
        c = RClient()
        data = c.rk_create(self.generator_image())
        if "Result" in data:
            trans = self.trans_captcha_results(','.join([str(int(v)-1) for v in data["Result"]]))
            self.results = trans
            return self.check(trans)
        else:
            if "Error" in data and data["Error"]:
                Log.e("打码平台错误: {0}, 请登录打码平台查看-http://www.ruokuai.com/client/index?6726".format(data["Error"]))
                return False, "若快打码平台错误"


    def verifyhandle_hand(self):
        img = Image.open(BytesIO(self.generator_image()))
        img.show()
        Log.v(
            """ 
            -----------------
            | 0 | 1 | 2 | 3 |
            -----------------
            | 4 | 5 | 6 | 7 |
            ----------------- """)
        results = input("输入验证码索引(见上图，以','分割）: ")
        img.close()
        trans = self.trans_captcha_results(results)
        self.results = trans
        return self.check(trans)

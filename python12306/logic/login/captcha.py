from io import BytesIO

from PIL import Image

from global_data.session import LOGIN_SESSION
from global_data.url_conf import LOGIN_URLMAPPING
from utils.log import Log

from utils.net import send_requests, json_status


class NormalCaptchaUtil(object):
    success_code = '4'

    @staticmethod
    def getcaptcha():
        img_binary = send_requests(LOGIN_SESSION, LOGIN_URLMAPPING["normal"]["captcha"])
        return img_binary

    def check(self, results):
        form_data = {
            'randCode': results,
            'rand': 'sjrand',
        }

        json_response = send_requests(LOGIN_SESSION,
                                      LOGIN_URLMAPPING["normal"]["captchaCheck"],
                                      data=form_data)
        Log.v('normal login captcha verify: %s' % json_response)
        return json_status(json_response, (), self.success_code)


class OtherCaptchaUtil(object):
    success_code = '1'

    @staticmethod
    def getcaptcha():
        img_binary = send_requests(LOGIN_SESSION, LOGIN_URLMAPPING["other"]["captcha"])
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

    def __init__(self, login_type):
        self.login_type = login_type
        self.util = self.captcha[self.login_type]

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

    def verify(self):
        # try five times.
        for v in range(5):
            try:
                img = Image.open(BytesIO(self.getcaptcha()))
                break
            except OSError:
                continue
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
        print(trans)
        return self.check(trans)

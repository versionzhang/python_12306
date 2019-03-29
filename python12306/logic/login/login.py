import ast
import re
import time
from urllib import parse

from selenium import webdriver

from python12306.global_data.session import LOGIN_SESSION
from python12306.global_data.const_data import DEVICE_FINGERPRINT

from python12306.config import Config
from python12306.global_data.url_conf import LOGIN_URL_MAPPING, DEVICE_FINGERPRINT_MAPPING
from python12306.logic.login.captcha import Captcha
from python12306.utils.log import Log
from python12306.utils.net import send_requests, json_status


class NormalLogin(object):
    __session = LOGIN_SESSION
    URLS = LOGIN_URL_MAPPING["normal"]

    def _init(self):
        Log.v("由于12306采取用设备指纹来校验访问, 现使用selenium获取完整cookie")
        options = webdriver.ChromeOptions()
        options.add_argument('headless')
        options.add_argument("-incognito")
        driver = webdriver.Chrome(options=options)
        driver.implicitly_wait(15)
        # first clear selenium cache
        driver.get("https://kyfw.12306.cn")
        time.sleep(3)
        cookies = driver.get_cookies()
        driver.quit()
        if "RAIL_DEVICEID" not in [v["name"] for v in cookies] \
            or "RAIL_EXPIRATION" not in [v["name"] for v in cookies]:
            return False, "设备指纹未获取到"
        for v in cookies:
            v.pop('httpOnly', None)
            v.pop('expiry', None)
            LOGIN_SESSION.cookies.set(**v)
        Log.v("已经获取设备指纹")
        return True, "已经获取设备指纹"

    def _get_device_fingerprint(self):
        if not hasattr(Config, "device_fingerprint"):
            query = dict(parse.parse_qsl(DEVICE_FINGERPRINT))
        else:
            query = dict(parse.parse_qsl(Config.device_fingerprint))
        query["timestamp"] = int(time.time() * 1000)
        data = send_requests(LOGIN_SESSION, DEVICE_FINGERPRINT_MAPPING, params=query)
        Log.d(data)
        if not data:
            return False, "获取设备ID请求失败"
        m = re.compile(r'callbackFunction\(\'(.*)\'\)')
        f = m.search(data)
        msg = "获取设备ID失败"
        if not f:
            Log.v(msg)
            return False, msg
        result = ast.literal_eval(f.group(1))
        # update cookie
        LOGIN_SESSION.cookies.update(
            {
                "RAIL_EXPIRATION": result.get("exp"),
                "RAIL_DEVICEID": result.get("dfp")
            }
        )
        Log.v("获取设备ID成功")
        return True, "OK"

    def _uamtk(self):
        json_data = send_requests(LOGIN_SESSION, self.URLS["uamtk"], data={'appid': 'otn'})
        Log.d(json_data)
        result, msg = json_status(json_data, ["result_message", "newapptk"])
        if not result:
            return result, msg, None
        else:
            return result, msg, json_data["newapptk"]

    def _passportredirect(self):
        send_requests(LOGIN_SESSION, self.URLS["userLoginRedirect"])

    def _uamauthclient(self, apptk):
        json_response = send_requests(LOGIN_SESSION, self.URLS['uamauthclient'], data={'tk': apptk})
        status, msg = json_status(json_response, ["username", "result_message"])
        if status:
            Log.v("欢迎 {0} 登录".format(json_response["username"]))
        return status, msg

    def login(self):
        if not LOGIN_SESSION.cookies.get("RAIL_EXPIRATION") or \
           not LOGIN_SESSION.cookies.get("RAIL_DEVICEID"):
            status, msg = self._init()
            if not status:
                return status, msg
        # status, msg = self._get_device_fingerprint()
        # if not status:
        #     Log.v("设备ID获取失败")
        #     return status, msg
        # self._init2()
        captcha = Captcha("normal")
        status, msg = captcha.verify()
        if not status:
            Log.v("验证码校验失败")
            return status, msg
        payload = {
            'username': Config.train_account.user,
            'password': Config.train_account.pwd,
            'appid': 'otn',
            'answer': captcha.results
        }
        json_response = send_requests(LOGIN_SESSION, self.URLS['login'], data=payload)
        result, msg = json_status(json_response, [], '0')
        if not result:
            return (False, json_response.get("result_message", None)) \
                if isinstance(json_response, dict) else (False, '登录接口提交返回数据出现问题')
        self._passportredirect()
        result, msg, apptk = self._uamtk()
        if not result:
            Log.v(msg)
            return False, msg
        status, msg = self._uamauthclient(apptk)
        return status, msg

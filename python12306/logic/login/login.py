from global_data.session import LOGIN_SESSION

from config import Config
from global_data.url_conf import LOGIN_URLMAPPING
from logic.login.captcha import Captcha
from utils.log import Log
from utils.net import send_requests, json_status


class NormalLogin(object):
    __session = LOGIN_SESSION
    URLS = LOGIN_URLMAPPING["normal"]

    def _init(self):
        send_requests(LOGIN_SESSION, self.URLS["init"])

    def _uamtk(self):
        json_data = send_requests(LOGIN_SESSION, self.URLS["uamtk"], data={'appid': 'otn'})
        Log.v(json_data)
        result, msg = json_status(json_data, ["result_message", "newapptk"])
        if not result:
            return result, msg, None
        else:
            return result, msg, json_data["newapptk"]

    def _passportredirect(self):
        send_requests(LOGIN_SESSION, self.URLS["userLoginRedirect"])

    def _uamauthclient(self, apptk):
        json_response = send_requests(LOGIN_SESSION, self.URLS['uamauthclient'], data={'tk': apptk})
        Log.v(json_response)
        return json_status(json_response, ["username", "result_message"])

    def login(self):
        self._init()
        captcha = Captcha("normal")
        status, msg = captcha.verify()
        if not status:
            Log.v("captcha verify failed")
            return status, msg
        payload = {
            'username': Config.train_account.user,
            'password': Config.train_account.pwd,
            'appid': 'otn',
            'answer': captcha.results
        }
        json_response = send_requests(LOGIN_SESSION, self.URLS['login'], data=payload)
        Log.v(json_response)
        result, msg = json_status(json_response, [], '0')
        if not result:
            return False, msg
        self._passportredirect()
        result, msg, apptk = self._uamtk()
        if not result:
            Log.v(msg)
            return False, msg
        status, msg = self._uamauthclient(apptk)
        return status, msg

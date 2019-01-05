from global_data.session import LOGIN_SESSION

from config import Config
from global_data.url_conf import LOGIN_URLMAPPING
from utils.net import send_requests, json_status


class NormalLogin(object):
    __session = LOGIN_SESSION
    URLS = LOGIN_URLMAPPING["normal"]

    def _init(self):
        send_requests(LOGIN_SESSION, self.URLS["init"])

    def _uamtk(self):
        json_data = send_requests(LOGIN_SESSION, self.URLS["uamtk"], data={'appid': 'otn'})
        return json_status(json_data, ["result_message", "newapptk"])

    def _uamauthclient(self, apptk):
        json_response = send_requests(LOGIN_SESSION, self.URLS['uamauthclient'], data={'tk': apptk})
        print(json_response)
        return json_status(json_response, ["username", "result_message"])

    def login(self):
        payload = {
            'username': Config.train_account.user,
            'password': Config.train_account.pwd,
            'appid': 'otn',
        }
        jsonRet = EasyHttp.send(self._urlInfo['login'], data=payload)

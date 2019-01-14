import datetime

from python12306.global_data.session import LOGIN_SESSION
from python12306.global_data.url_conf import USER_CHECK_URL_MAPPING
from python12306.utils.net import send_requests, submit_response_checker


class OnlineChecker(object):

    def __init__(self):
        self.check_time = datetime.datetime.now()

    def update_check_time(self):
        self.check_time = datetime.datetime.now()

    def should_check_online(self, current_time, delta_time=2):
        """
        :param current_time: 当前时间
        :param delta_time: 间隔时间, 单位为分钟
        :return:
        """
        delta = datetime.timedelta(minutes=delta_time)
        if current_time - self.check_time > delta:
            return True
        else:
            return False

    @staticmethod
    def checker():
        data = {
            '_json_att': ''
        }
        json_response = send_requests(LOGIN_SESSION, USER_CHECK_URL_MAPPING, data=data)
        status, msg = submit_response_checker(json_response, ["status", "data.flag"], True,
                                              "用户在线状态检测: 在线检测通过")
        return status, msg


OnlineCheckerTool = OnlineChecker()

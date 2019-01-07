import datetime
import re
import time
import urllib.parse

from config import Config
from global_data.const_data import find_by_name
from global_data.session import LOGIN_SESSION
from global_data.url_conf import SUBMIT_URL_MAPPING
from utils.log import Log
from utils.net import send_requests, submit_response_checker


class NormalSubmitDcOrder(object):
    """
    单程票正常订单提交类
    """
    URLS = SUBMIT_URL_MAPPING["dc"]
    token = ''
    passenger_data = []

    def __init__(self, train_detail):
        self.train = train_detail

    @staticmethod
    def decode_secret_str(string):
        return urllib.parse.unquote(string).replace('\n', '')

    @staticmethod
    def format_date(date):
        return datetime.datetime.strptime(date, '%Y%m%d').strftime('%Y-%m-%d')

    def _submit_order_request(self):
        """
        :param tour_flag:
        :return:
        """
        form_data = {
            'secretStr': self.decode_secret_str(self.train.secretStr),
            'train_date': self.format_date(self.train.train_date),  # 车票时间
            'back_train_date': time.strftime("%Y-%m-%d", time.localtime()),  # query date:2017-12-31
            'tour_flag': 'dc',
            'purpose_codes': find_by_name("ticket", Config.basic_config.ticket_type).sys_code,
            'query_from_station_name': self.train.from_station_code,
            'query_to_station_name': self.train.to_station_code,
            'undefined': '',
        }
        json_response = send_requests(LOGIN_SESSION, self.URLS['submitOrderRequest'], data=form_data)
        Log.v('submitOrderRequest %s' % json_response)
        return submit_response_checker(json_response, ["status"], True)

    def _get_submit_token(self):
        html = send_requests(LOGIN_SESSION, self.URLS['getExtraInfo'])
        Log.v("获取globalRepeatSubmitToken,用于订单提交")
        result = re.findall(r"var globalRepeatSubmitToken = '(.*)'", html)
        if result:
            self.token = result[0]
            return True
        else:
            return False

    def _get_passenger_data(self):
        # get token from
        while not self.token:
            self._get_submit_token()
        # 获取乘客信息并保存
        while not self.passenger_data:
            form_data = {
                '_json_att': '',
                'REPEAT_SUBMIT_TOKEN': self.token
            }
            json_response = send_requests(LOGIN_SESSION, self.URLS['getPassengerDTOs'], data=form_data)
            Log.v('获取乘客信息 %s' % json_response)
            status, msg = submit_response_checker(json_response, ["status"], True)
            if status:
                # write data to passger data.
                return True, "OK"



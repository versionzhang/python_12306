import datetime
import json
import re
import time
import urllib.parse

from config import Config
from global_data.const_data import find_by_name
from global_data.session import LOGIN_SESSION
from global_data.url_conf import SUBMIT_URL_MAPPING
from pre_processing.passengers import PassengerData
from utils.log import Log
from utils.lookup import build_passenger_ticket_string, build_oldpassenger_ticket_string, BlackTrains
from utils.net import send_requests, submit_response_checker

NORMAL_PIPELINE = [
    "_submit_order_request",
    "_get_passenger_data",
    "_check_order_info",
    "_get_queue_count",
    "_confirm_single_or_go_for_queue",
    "_wait_for_order_id",
    "_check_order_status_queue"
]


class NormalSubmitDcOrder(object):
    """
    单程票正常订单提交类
    """
    URLS = SUBMIT_URL_MAPPING["dc"]
    token = ''
    ticket_passenger_info = {}
    passenger_data = []
    left_tickets = -1
    wait_time = 120
    order_id = ''
    retry_time = 2

    def __init__(self, train_detail, seat_type):
        self.train = train_detail
        self.seat_type = seat_type

    @staticmethod
    def decode_secret_str(string):
        return urllib.parse.unquote(string).replace('\n', '')

    @staticmethod
    def format_date(date):
        return datetime.datetime.strptime(date, '%Y%m%d').strftime('%Y-%m-%d')

    def _submit_order_request(self):
        """
        :return:
        """
        form_data = {
            'secretStr': self.decode_secret_str(self.train.secretStr.value),
            'train_date': self.format_date(self.train.train_date.value),  # 车票时间
            'back_train_date': time.strftime("%Y-%m-%d", time.localtime()),  # query date:2017-12-31
            'tour_flag': 'dc',
            'purpose_codes': find_by_name("ticket", Config.basic_config.ticket_type).sys_code,
            'query_from_station_name': self.train.from_station_code.value,
            'query_to_station_name': self.train.to_station_code.value,
            'undefined': '',
        }
        json_response = send_requests(LOGIN_SESSION, self.URLS['submitOrderRequest'], data=form_data)
        Log.v('submitOrderRequest %s' % json_response)
        return submit_response_checker(json_response, ["status"], True)

    def _get_submit_token(self):
        html = send_requests(LOGIN_SESSION, self.URLS['getExtraInfo'])
        Log.v("获取globalRepeatSubmitToken,用于订单提交")
        result = re.findall(r"var globalRepeatSubmitToken = '(.*)'", html)
        ticket_passenger_info = re.findall(r'var ticketInfoForPassengerForm=(.*);', html)
        if result:
            self.token = result[0]
        if ticket_passenger_info:
            try:
                self.ticket_passenger_info = json.loads(ticket_passenger_info[0].replace("'", "\""))
            except TypeError:
                Log.w("获取submit info失败")
                return False
        if self.token and self.ticket_passenger_info:
            return True
        else:
            return False

    def _get_passenger_data(self):
        if PassengerData.passenger:
            self.passenger_data = PassengerData.find_people_by_names(Config.basic_config.ticket_people_list)
            Log.v(self.passenger_data)
            # get token from html file.
            while True:
                if self.token and self.ticket_passenger_info:
                    break
                else:
                    self._get_submit_token()
            return True, "使用缓存的文件内容获取成功"
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
                # write data to passenger data.
                PassengerData.raw_data = json_response['data']['normal_passengers']
                PassengerData.get_final_data()
                self.passenger_data = PassengerData.find_people_by_names(Config.basic_config.ticket_people_list)
                while True:
                    if self.token and self.ticket_passenger_info:
                        break
                    else:
                        self._get_submit_token()
                return True, "OK"
            else:
                return False, "获取乘客信息失败"

    def _check_order_info(self):
        form_data = {
            'cancel_flag': self.ticket_passenger_info['orderRequestDTO']['cancel_flag'] or '2',
            'bed_level_order_num': self.ticket_passenger_info['orderRequestDTO']['bed_level_order_num'] \
                                   or '000000000000000000000000000000',
            'passengerTicketStr': build_passenger_ticket_string(self.seat_type, self.passenger_data),
            'oldPassengerStr': build_oldpassenger_ticket_string(self.passenger_data),
            'tour_flag': self.ticket_passenger_info['tour_flag'] or 'dc',
            'randCode': '',
            'whatsSelect': '1',
            '_json_att': '',
            'REPEAT_SUBMIT_TOKEN': self.token,
        }
        Log.v('send form data to check_order_info url %s' % form_data)
        json_response = send_requests(LOGIN_SESSION, self.URLS['checkOrderInfo'], data=form_data)
        Log.v('校验订单信息返回json数据 %s' % json_response)
        status, msg = submit_response_checker(json_response, ["status", "data.submitStatus"], True)
        return status, msg

    def _get_queue_count(self):
        form_data = {
            'train_date': datetime.datetime.strptime(
                self.ticket_passenger_info['queryLeftTicketRequestDTO']['train_date'], '%Y%m%d').strftime(
                '%b %a %d %Y 00:00:00 GMT+0800') + ' (中国标准时间)',
            'train_no': self.ticket_passenger_info['queryLeftTicketRequestDTO']['train_no'],
            'stationTrainCode': self.train.stationTrainCode.value,
            'seatType': self.seat_type.sys_code,
            'fromStationTelecode': self.train.from_station_code.value,
            'toStationTelecode': self.train.to_station_code.value,
            'leftTicket': self.ticket_passenger_info['leftTicketStr'],
            'purpose_codes': self.ticket_passenger_info['purpose_codes'],
            'train_location': self.ticket_passenger_info['train_location'],
            '_json_att': '',
            'REPEAT_SUBMIT_TOKEN': self.token
        }
        Log.v('send post data to get_queue_count {data}'.format(data=form_data))
        json_response = send_requests(LOGIN_SESSION, self.URLS['getQueueCount'], data=form_data)
        Log.v('get_queue_count 返回json数据 %s' % json_response)
        status, msg = submit_response_checker(json_response, ["status"], True)
        if status:
            self.left_tickets = json_response['data']['ticket']
        else:
            BlackTrains.add_train(self.train)
        return status, msg

    def _confirm_single_or_go_for_queue(self):
        form_data = {
            'passengerTicketStr': build_passenger_ticket_string(self.seat_type, self.passenger_data),
            'oldPassengerStr': build_oldpassenger_ticket_string(self.passenger_data),
            'randCode': '',
            'purpose_codes': self.ticket_passenger_info['purpose_codes'],
            'key_check_isChange': self.ticket_passenger_info['key_check_isChange'],
            'leftTicketStr': self.ticket_passenger_info['leftTicketStr'],
            'train_location': self.ticket_passenger_info['train_location'],
            'choose_seats': '',  # 暂时未加选座
            'seatDetailType': '000',
            'whatsSelect': '1',
            'roomType': '00',
            'dwAll': 'N',
            '_json_att': '',
            'REPEAT_SUBMIT_TOKEN': self.token,
        }
        json_response = send_requests(LOGIN_SESSION, self.URLS['confirmForQueue'], data=form_data)
        Log.v('confirm_single_or_go_for_queue 返回json数据 %s' % json_response)
        status, msg = submit_response_checker(json_response, ["status", "data.submitStatus"], True)
        return status, msg

    def _query_order_wait_time(self):
        params = {
            'random': '%10d' % (time.time() * 1000),
            'tourFlag': self.ticket_passenger_info['tour_flag'] or 'dc',
            '_json_att': '',
            'REPEAT_SUBMIT_TOKEN': self.token
        }
        json_response = send_requests(LOGIN_SESSION, self.URLS['queryOrderWaitTime'], params=params)
        Log.v('query_order_wait_time 返回json数据 %s' % json_response)
        status, msg = submit_response_checker(json_response, ["status"], True)
        if status:
            self.wait_time = json_response['data']['waitTime']
            self.order_id = json_response['data']['orderId']
        return status, msg

    def _wait_for_order_id(self):
        # 排队逻辑
        t = datetime.datetime.now()
        delta = datetime.timedelta(minutes=10)
        while self.wait_time and self.wait_time >= 0:
            loop_time = datetime.datetime.now()
            status, msg = self._query_order_wait_time()
            time.sleep(5)
            if self.order_id:
                return True, "OK"
            if loop_time > t + delta:
                return False, "提交超时"

    def _check_order_status_queue(self):
        params = {
            'orderSequence_no': self.order_id,
            '_json_att': '',
            'REPEAT_SUBMIT_TOKEN': self.token,
        }
        json_response = send_requests(LOGIN_SESSION, self.URLS['resultOrderForQueue'], params=params)
        Log.v('check_order_status_queue 返回json数据 %s' % json_response)
        status, msg = submit_response_checker(json_response, ["status", "data.submitStatus"], True)
        return status, msg

    def run(self):
        while self.retry_time:
            for v in NORMAL_PIPELINE:
                status, msg = getattr(self, v)()
                if not status:
                    self.retry_time -= 1
                    break
            else:
                Log.v("提交订单成功")
                return True
        Log.v("提交订单失败")
        return False

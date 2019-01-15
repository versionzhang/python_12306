import datetime
import time
from collections import OrderedDict
from urllib.parse import unquote

from python12306.config import Config
from python12306.global_data.const_data import find_by_name
from python12306.global_data.session import LOGIN_SESSION
from python12306.global_data.url_conf import FAST_SUBMIT_URL_MAPPING
from python12306.logic.login.passager import QueryPassengerTool
from python12306.logic.submit.submit import NormalSubmitDcOrder
from python12306.utils.log import Log
from python12306.utils.lookup import build_passenger_ticket_string, build_oldpassenger_ticket_string, BlackTrains
from python12306.utils.net import send_requests, submit_response_checker

FAST_PIPELINE = [
    "_get_passenger_data",
    "_auto_submit_order_request",
    "_get_queue_count_async",
    "_confirm_single_for_queue_asys",
    "_wait_for_order_id",
    "_check_order_status_queue"
]


class FastSubmitDcOrder(NormalSubmitDcOrder):
    """
    单程票快速订单提交类
    """
    URLS = FAST_SUBMIT_URL_MAPPING
    token = ''
    ticket_passenger_info = {}
    passenger_data = []
    left_tickets = -1
    wait_time = 120
    order_id = ''
    retry_time = 1

    def _get_passenger_data(self):
        self.passenger_data = QueryPassengerTool.config_passengers
        return True, "获取乘客信息成功"

    def _auto_submit_order_request(self):
        """
        :return: status, msg
        """
        data = OrderedDict()
        data["secretStr"] = self.decode_secret_str(self.train.secretStr.value)
        data["train_date"] = self.format_date(self.train.train_date.value)
        data["tour_flag"] = "dc"
        data["purpose_codes"] = find_by_name("ticket", Config.basic_config.ticket_type).sys_code
        data["query_from_station_name"] = self.train.from_station.value.name
        data["query_to_station_name"] = self.train.to_station.value.name
        data["cancel_flag"] = 2
        data["bed_level_order_num"] = "000000000000000000000000000000"
        data["passengerTicketStr"] = build_passenger_ticket_string(self.seat_type, self.passenger_data)
        data["oldPassengerStr"] = build_oldpassenger_ticket_string(self.passenger_data)
        json_response = send_requests(LOGIN_SESSION, self.URLS['autoSubmitOrderRequest'], data=data)
        status, msg = submit_response_checker(json_response, ["status", "data.submitStatus"], True)
        if status:
            self.ticket_passenger_info = dict(zip(["train_location", "key_check_isChange", "leftTicketStr"],
                                                  [unquote(v) for v in json_response["data"]["result"].split("#")]))
        return status, msg

    def _get_queue_count_async(self):
        form_data = {
            'train_date': datetime.datetime.strptime(
                self.train.train_date.value, '%Y%m%d').strftime(
                '%b %a %d %Y 00:00:00 GMT+0800') + ' (中国标准时间)',
            'train_no': self.train.sys_train_no.value,
            'stationTrainCode': self.train.stationTrainCode.value,
            'seatType': self.seat_type.sys_code,
            'fromStationTelecode': self.train.from_station_code.value,
            'toStationTelecode': self.train.to_station_code.value,
            'leftTicket': self.ticket_passenger_info['leftTicketStr'],
            'purpose_codes': find_by_name("ticket", Config.basic_config.ticket_type).sys_code,
            '_json_att': ''
        }
        json_response = send_requests(LOGIN_SESSION, self.URLS['getQueueCountAsync'], data=form_data)
        status, msg = submit_response_checker(json_response, ["status"], True)
        if not status:
            BlackTrains.add_train(self.train)
        return status, msg

    def _confirm_single_for_queue_asys(self):
        form_data = OrderedDict()
        form_data['passengerTicketStr'] = build_passenger_ticket_string(self.seat_type, self.passenger_data)
        form_data['oldPassengerStr'] = build_oldpassenger_ticket_string(self.passenger_data)
        form_data['randCode'] = ''
        form_data['purpose_codes'] = find_by_name("ticket", Config.basic_config.ticket_type).sys_code
        form_data['key_check_isChange'] = self.ticket_passenger_info['key_check_isChange']
        form_data['leftTicketStr'] = self.ticket_passenger_info['leftTicketStr']
        form_data['train_location'] = self.ticket_passenger_info['train_location']
        form_data['choose_seats'] = ''
        form_data['seatDetailType'] = ''
        form_data['_json_att'] = ''
        json_response = send_requests(LOGIN_SESSION, self.URLS['confirmSingleForQueueAsys'], data=form_data)
        status, msg = submit_response_checker(json_response, ["status", "data.submitStatus"], True)
        return status, msg

    def _query_order_wait_time(self):
        params = {
            'random': '%10d' % (time.time() * 1000),
            'tourFlag': 'dc',
            '_json_att': ''
        }
        json_response = send_requests(LOGIN_SESSION, self.URLS['queryOrderWaitTime'], params=params)
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
            self._query_order_wait_time()
            time.sleep(5)
            if self.order_id:
                return True, "OK"
            if loop_time > t + delta:
                return False, "提交超时"

    def _check_order_status_queue(self):
        params = {
            'orderSequence_no': self.order_id,
            '_json_att': ''
        }
        json_response = send_requests(LOGIN_SESSION, self.URLS['resultOrderForQueue'], params=params)
        status, msg = submit_response_checker(json_response, ["status", "data.submitStatus"], True)
        return status, msg

    def run(self):
        while self.retry_time:
            for v in FAST_PIPELINE:
                status, msg = getattr(self, v)()
                if not status:
                    self.retry_time -= 1
                    break
            else:
                Log.v("提交订单成功")
                return True
        Log.v("提交订单失败")
        return False

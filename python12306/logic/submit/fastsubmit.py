import datetime
import time
from collections import OrderedDict

from config import Config
from global_data.const_data import find_by_name
from global_data.session import LOGIN_SESSION
from global_data.url_conf import FAST_SUBMIT_URL_MAPPING
from pre_processing.passengers import PassengerData
from logic.submit.submit import NormalSubmitDcOrder
from utils.log import Log
from utils.lookup import build_passenger_ticket_string, build_oldpassenger_ticket_string, BlackTrains
from utils.net import send_requests, submit_response_checker

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
    单程票正常订单提交类
    """
    URLS = FAST_SUBMIT_URL_MAPPING
    token = ''
    ticket_passenger_info = {}
    passenger_data = []
    left_tickets = -1
    wait_time = 120
    order_id = ''
    retry_time = 2

    def _auto_submit_order_request(self):
        data = OrderedDict()
        data["secretStr"] = self.decode_secret_str(self.train.secretStr.value)
        data["train_date"] = self.format_date(self.train.train_date.value)
        data["tour_flag"] = "dc"
        data["purpose_codes"] = find_by_name("ticket", Config.basic_config.ticket_type).sys_code
        data["query_from_station_name"] = self.train.from_station_code.value
        data["query_to_station_name"] = self.train.to_station_code.value
        data["cancel_flag"] = 2
        data["bed_level_order_num"] = "000000000000000000000000000000"
        data["passengerTicketStr"] = build_passenger_ticket_string(self.seat_type, self.passenger_data)
        data["oldPassengerStr"] = build_oldpassenger_ticket_string(self.passenger_data)
        json_response = send_requests(LOGIN_SESSION, self.URLS['autoSubmitOrderRequest'], data=data)
        Log.v('auto submitOrderRequest %s' % json_response)
        return submit_response_checker(json_response, ["status"], True)

    def _get_queue_count_async(self):
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
            '_json_att': ''
        }
        json_response = send_requests(LOGIN_SESSION, self.URLS['getQueueCountAsync'], data=form_data)
        Log.v('get_queue_count_async 返回json数据 %s' % json_response)
        status, msg = submit_response_checker(json_response, ["status"], True)
        if status:
            self.left_tickets = json_response['data']['ticket']
        else:
            BlackTrains.add_train(self.train)
        return status, msg

    def _confirm_single_for_queue_asys(self):
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
            '_json_att': '',
        }
        json_response = send_requests(LOGIN_SESSION, self.URLS['confirmSingleForQueueAsys'], data=form_data)
        Log.v('confirm_single_or_go_for_queue 返回json数据 %s' % json_response)
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

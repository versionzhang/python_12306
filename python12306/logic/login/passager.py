from python12306.global_data.session import LOGIN_SESSION

from python12306.config import Config
from python12306.global_data.url_conf import PASSENGER_URL_MAPPING
from python12306.pre_processing.passengers import PassengerData
from python12306.utils.log import Log
from python12306.utils.net import send_requests, submit_response_checker


class QueryPassengersData(object):
    def __init__(self):
        self.passengers = []
        self.config_passengers = []

    def query(self):
        # 乘客信息最多十五个
        retry = 3
        while retry:
            json_response = send_requests(LOGIN_SESSION,
                                          PASSENGER_URL_MAPPING,
                                          data={"pageIndex": 1,
                                                "pageSize": 10})
            status, msg = submit_response_checker(json_response, ["status", "data.flag"], True)
            if not status:
                self.passengers = []
                retry -= 1
                Log.v("获取乘客信息失败, 重试中")
                continue
            else:
                self.passengers.extend(json_response["data"]["datas"])
            p2_json_response = send_requests(LOGIN_SESSION,
                                             PASSENGER_URL_MAPPING,
                                             data={"pageIndex": 2,
                                                   "pageSize": 10})
            status, msg = submit_response_checker(p2_json_response, ["status", "data.flag"], True)
            if not status:
                self.passengers = []
                retry -= 1
                Log.v("获取乘客信息失败, 重试中")
                continue
            else:
                self.passengers.extend(p2_json_response["data"]["datas"])
            break
        if not self.passengers:
            return False
        Log.v("获取乘客信息成功")
        return True

    def filter_by_config(self):
        status = self.query()
        if not status:
            Log.e("未能获取乘客信息, 请重试")
        PassengerData.raw_data = self.passengers
        PassengerData.get_final_data()
        data = PassengerData.find_people_by_names(Config.basic_config.ticket_people_list)
        if len(data) == 0:
            Log.e("乘客信息未在账号中找到, 请检查")
            return False
        if len(data) != len(Config.basic_config.ticket_people_list):
            Log.w("乘客信息配置中包含错误, 已经滤除错误乘客")
        self.config_passengers = data
        return True


QueryPassengerTool = QueryPassengersData()

import copy
from itertools import chain

from prettytable import PrettyTable

from config import Config
from global_data.const_data import find_by_name, find_by_names
from global_data.url_conf import QUERY_URL_MAPPING
from pre_processing.cities import CityData
from utils.log import Log

from global_data.session import LOGIN_SESSION
from utils.net import send_requests

from utils.data_structure import TrainDetail


class Query(object):

    def __init__(self, travel_date):
        self.travel_date = travel_date

    def run_query(self):
        params = {
            r'leftTicketDTO.train_date': self.travel_date,
            r'leftTicketDTO.from_station': CityData.find_city_by_name(Config.basic_config.from_station).code,
            r'leftTicketDTO.to_station': CityData.find_city_by_name(Config.basic_config.to_station).code,
            r'purpose_codes': find_by_name("ticket", Config.basic_config.ticket_type).sys_code
        }
        json_response = send_requests(LOGIN_SESSION, QUERY_URL_MAPPING, params=params)
        if not isinstance(json_response, (list, dict)):
            return []
        return [TrainDetail(v.split('|')) for v in json_response['data']['result']] or []

    @staticmethod
    def pretty_output(t):
        table = PrettyTable()
        table.field_names = [getattr(t, v).verbose for v in t.__slots__ if getattr(t, v).display]
        fields = [v for v in t.__slots__ if getattr(t, v).display]
        table.add_row([getattr(t, v).value if isinstance(getattr(t, v).value, str) and getattr(t, v).display
                       else getattr(t, v).value.name for v in fields]
                      )
        print(table)

    def output_to_console(self, data):
        for v in data:
            self.pretty_output(v)

    def filter(self):
        data = self.run_query()
        q = QueryFilter(data)
        return q.filter()


class QueryFilter(object):

    def __init__(self, data):
        self.data = data
        self.enough_result = []
        self.may_not_enough_result = []
        self.result = []

    def filter_by_seat(self):
        seat_objs = find_by_names('seat', Config.basic_config.ticket_types)
        for v in seat_objs:
            for v1 in self.data:
                for p in v1.__slots__:
                    if isinstance(getattr(v1, p).value, str) and \
                            getattr(v1, p).verbose == v.name and getattr(v1, p).value:
                        if getattr(v1, p).value == '有':
                            self.enough_result.append([v, copy.copy(v1)])
                        if getattr(v1, p).value.isnumeric():
                            self.may_not_enough_result.append([v, copy.copy(v1)])
        # 按照余票信息重新排序, 显示为有的放前面, 按照设定的席别进行排序
        self.enough_result = [[v1 for v1 in self.enough_result if v1[0] == v]for v in seat_objs]
        self.may_not_enough_result = [[v1 for v1 in self.may_not_enough_result if v1[0] == v] for v in seat_objs]
        self.result = list(chain(*[v + self.may_not_enough_result[index] for index, v in enumerate(self.enough_result)]))

    def filter_train_time(self):
        return list(
            filter(
                lambda x: Config.basic_config.earliest_time < x[1].start_time.value \
                          and x[1].arrive_time.value < Config.basic_config.latest_time,
                self.result)
        )

    def filter_train_type(self):
        return list(
            filter(
                lambda x: x[1].stationTrainCode.value[0] in Config.basic_config.train_types or \
                          (x[1].stationTrainCode.value[0].isnumeric() and 'S' in Config.basic_config.train_types),
                self.result)
        )

    def filter_train_num(self):
        return list(
            filter(
                lambda x: x[1].stationTrainCode.value in Config.basic_config.train_list,
                self.result)
        )

    def filter(self):
        # 先过滤席位
        self.filter_by_seat()
        if self.result:
            Log.v("查找到符合配置的车次信息: {0}".format(','.join(
                [v[1].stationTrainCode.value for v in self.result])))
        if Config.basic_config.manual_trainnum_enable:
            self.result = self.filter_train_num()
        else:
            self.result = self.filter_train_time()
            self.result = self.filter_train_type()
        return self.result

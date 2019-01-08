import copy

from prettytable import PrettyTable

from config import Config
from global_data.const_data import find_by_name, find_by_names
from global_data.url_conf import QUERY_URL_MAPPING
from pre_processing.citys import CityData
from utils.log import Log

from global_data.session import LOGIN_SESSION
from utils.net import send_requests

from utils.data_structure import TrainDetail


class Query(object):

    @staticmethod
    def run_query():
        params = {
            r'leftTicketDTO.train_date': Config.basic_config.travel_dates,
            r'leftTicketDTO.from_station': CityData.find_city_by_name(Config.basic_config.from_station).code,
            r'leftTicketDTO.to_station': CityData.find_city_by_name(Config.basic_config.to_station).code,
            r'purpose_codes': find_by_name("ticket", Config.basic_config.ticket_type).sys_code
        }
        Log.v(params)
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
        q.filter_by_seat()
        self.pretty_output(q.result[0])
        return q.result[0]
        # for v in q.result:
        #     self.pretty_output(v)



class QueryFilter(object):
    def __init__(self, data):
        self.data = data
        self.result = []

    def filter_by_seat(self):
        seat_objs = find_by_names('seat', Config.basic_config.ticket_types)
        for v in seat_objs:
            for v1 in self.data:
                for p in v1.__slots__:
                    if isinstance(getattr(v1, p).value, str) and \
                        getattr(v1, p).verbose == v.name and getattr(v1, p).value and getattr(v1, p).value != '无':
                            self.result.append(copy.copy(v1))

    # def filter_train_type(self):
    #     return
    #
    # def filter_train_num(self):
    #     return

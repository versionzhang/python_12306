from prettytable import PrettyTable

from config import Config
from global_data.const_data import find_by_name
from global_data.url_conf import QUERY_URL_MAPPING
from logic.login.login import NormalLogin
from pre_processing.citys import CityData
from utils.log import Log

from global_data.session import LOGIN_SESSION
from utils.net import send_requests

from utils.data_structure import TrainDetail


class Query(object):
    # TODO: add filter to query.
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
        return json_response['data']['result'] or []

    @staticmethod
    def pretty_output(raw_train_data):
        table = PrettyTable()
        t = TrainDetail(raw_train_data.split('|'))
        table.field_names = [getattr(t, v).verbose for v in t.__slots__ if getattr(t, v).display]
        fields = [v for v in t.__slots__ if getattr(t, v).display]
        table.add_row([getattr(t, v).value if isinstance(getattr(t, v).value, str) and getattr(t, v).display
                       else getattr(t, v).value.name for v in fields]
                      )
        print(table)

    def output_to_console(self):
        data = self.run_query()
        for v in data:
            self.pretty_output(v)

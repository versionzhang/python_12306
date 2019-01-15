import datetime

from python12306.config import Config
from python12306.global_data.const_data import find_by_name


def build_passenger_ticket_string(seat_type, passengers):
    # 1(seatType),0,1(车票类型:ticket_type_codes),张三(passenger_name),1(证件类型:passenger_id_type_code),320xxxxxx(passenger_id_no),151xxxx(mobile_no),N
    f = lambda x: '%s,0,%s,%s,%s,%s,%s,N' % (seat_type.sys_code,
                                             find_by_name("ticket", Config.basic_config.ticket_type).user_code,
                                             x.passenger_name,
                                             x.passenger_id_type_code,
                                             x.passenger_id_no,
                                             x.mobile_no)
    return '_'.join([f(v) for v in passengers])


def build_oldpassenger_ticket_string(passengers):
    # oldPassengerStr-->张三(passenger_name),1(证件类型:passenger_id_type_code),320xxxxxx(passenger_id_no),1_
    f = lambda x: '%s,%s,%s,%s_' % (x.passenger_name,
                                    x.passenger_id_type_code,
                                    x.passenger_id_no,
                                    find_by_name("ticket", Config.basic_config.ticket_type).user_code)
    return '_'.join([f(v) for v in passengers])


class BlackTrainList(object):
    def __init__(self):
        self.trains = []

    def add_train(self, train):
        now = datetime.datetime.now()
        self.trains.append([now, train])

    def check(self, train_obj):
        now = datetime.datetime.now()
        # 过滤掉已经过期的数据
        self.trains = list(
            filter(lambda x: datetime.timedelta(minutes=Config.basic_config.black_train_time) + x[0] > now,
                   self.trains))
        for v in self.trains:
            if v[1].sys_train_no.value == train_obj.sys_train_no.value and \
                    v[1].train_date.value == train_obj.train_date.value:
                return True
        return False


BlackTrains = BlackTrainList()

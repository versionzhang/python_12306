from config import Config
from global_data.const_data import find_by_name


def build_passenger_ticket_string(seat_type, passengers):
    # 1(seatType),0,1(车票类型:ticket_type_codes),张三(passenger_name),1(证件类型:passenger_id_type_code),320xxxxxx(passenger_id_no),151xxxx(mobile_no),N
    f = lambda x: '%s,0,%s,%s,%s,%s,%s,N' % (seat_type,
                                      find_by_name("ticket", Config.basic_config.ticket_type).user_code,
                                      x.passenger_name,
                                      x.passenger_id_type_code,
                                      x.passenger_id_no,
                                      x.mobile_no)
    return '_'.join([f(v) for v in passengers])


def build_oldpassenger_ticket_string(passengers):
    # oldPassengerStr-->张三(passenger_name),1(证件类型:passenger_id_type_code),320xxxxxx(passenger_id_no),1_
    f = lambda x: '%s,%s,%s,1_' % (x.passenger_name,
                                   x.passenger_id_type_code,
                                   x.passenger_id_no)
    return '_'.join([f(v) for v in passengers])

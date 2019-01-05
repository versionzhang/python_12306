from utils.data_structure import TourMapping, SeatMapping, TicketMapping

TYPE_LOGIN_NORMAL_WAY = 0
TYPE_LOGIN_OTHER_WAY = 1

TOUR_DATA = [
    {
        "name": "单程",
        "sys_code": "dc"
    },
    {
        "name": "往返",
        "sys_code": "wc"
    }
]

SEAT_DATA = [
    {
        "name": '商务座',
        "sys_code": '9'
    },
    {
        "name": '特等座',
        "sys_code": 'P'
    },
    {
        "name": '一等座',
        "sys_code": 'M'
    },
    {
        "name": '二等座',
        "sys_code": 'O'
    },
    {
        "name": '高级软卧',
        "sys_code": '6'
    },
    {
        "name": '软卧',
        "sys_code": '4'
    },
    {
        "name": '硬卧',
        "sys_code": '3'
    },
    {
        "name": '软座',
        "sys_code": '2'
    },
    {
        "name": '硬座',
        "sys_code": '1'
    },
    {
        "name": '无座',
        "sys_code": '1'
    }
]

TICKET_DATA = [
    {
        "name": "成人票",
        "user_code": '1',
        "sys_code": "ADULT"
    },
    {
        "name": "儿童票",
        "user_code": '2',
        "sys_code": ""
    },
    {
        "name": "学生票",
        "user_code": '3',
        "sys_code": "0X00"
    },
    {
        "name": "残军票",
        "user_code": '4',
        "sys_code": ""
    }
]

TourTypeList  = [ TourMapping(v) for v in TOUR_DATA]
SeatTypeList = [ SeatMapping(v) for v in SEAT_DATA]
TicketTypeList = [ TicketMapping(v) for v in TICKET_DATA]

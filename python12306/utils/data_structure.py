class BasicMapping(object):
    def __init__(self, data):
        for attr, v in data.items():
            setattr(self, attr, v)

    def __str__(self):
        return str(type(self)) + ' '.join(["{attr}:{val}".format(attr=v, val=getattr(self, v)) for v in self.__slots__])

    __repr__ = __str__


class CityStationMapping(BasicMapping):
    __slots__ = (
        "abbr3",
        "name",
        "code",
        "pinyin",
        "abbr2",
        "num"
    )


class TourMapping(BasicMapping):
    __slots__ = (
        "name",
        "sys_code"
    )


class SeatMapping(BasicMapping):
    __slots__ = (
        "name",
        "sys_code"
    )


class TicketMapping(BasicMapping):
    __slots__ = (
        "name",
        "user_code",
        "sys_code"
    )


class UrlMapping(object):
    __slots__ = (
        'url', 'method', 'headers', 'response'
    )

    def __init__(self, data):
        for attr, v in data.items():
            if callable(v):
                setattr(self, attr, v())
            else:
                setattr(self, attr, v)
        for v in self.__slots__:
            # default value data.
            if not getattr(self, v, None):
                if v == 'method':
                    setattr(self, v, 'GET')
                if v == 'response':
                    setattr(self, v, 'json')
                if v == 'headers':
                    setattr(self, v, {})

    def __str__(self):
        return str(type(self)) + ' '.join([
            "{attr}:{val}".format(attr=v, val=getattr(self, v)) for v in self.__slots__])

    __repr__ = __str__


TRAIN_MAPPING = [
    {
        "index": 0,
        "name": "secretStr",
        "verbose": "秘密字符串",
        "display": False
    },
    # 1 备注 2 预订
    {
        "index": 2,
        "name": "sys_train_no",
        "verbose": "车次代码",
        "display": False
    },
    {
        "index": 3,
        "name": "stationTrainCode",
        "verbose": "车次",
    },
    # 起始站
    {
        "index": 4,
        "name": "start_station_code",
        "verbose": "始发站代码",
        "display": False
    },
    {
        "index": 5,
        "name": "end_station_code",
        "verbose": "终点站代码",
        "display": False
    },
    {
        "index": 6,
        "name": "from_station_code",
        "verbose": "出发站代码",
        "display": False
    },
    {
        "index": 7,
        "name": "to_station_code",
        "verbose": "到达站代码",
        "display": False
    },
    {
        "index": 8,
        "name": "start_time",
        "verbose": "出发时间"
    },
    {
        "index": 9,
        "name": "arrive_time",
        "verbose": "到达时间"
    },
    {
        "index": 10,
        "name": "total_time",
        "verbose": "总时长"
    },
    {
        "index": 13,
        "name": "train_date",
        "verbose": "车票出发日期"
    },
    {
        "index": 32,
        "name": "business_seat",
        "verbose": "商务特等座",
        "display": False
    },
    {
        "index": 31,
        "name": "first_class_seat",
        "verbose": "一等座"
    },
    {
        "index": 30,
        "name": "second_class_seat",
        "verbose": "二等座"
    },
    {
        "index": 21,
        "name": "advanced_soft_sleep",
        "verbose": "高级软卧",
        "display": False
    },
    {
        "index": 23,
        "name": "soft_sleep",
        "verbose": "软卧"
    },
    {
        "index": 33,
        "name": "move_sleep",
        "verbose": "动卧",
        "display": False
    },
    {
        "index": 28,
        "name": "hard_sleep",
        "verbose": "硬卧"
    },
    {
        "index": 24,
        "name": "soft_seat",
        "verbose": "软座"
    },
    {
        "index": 29,
        "name": "hard_seat",
        "verbose": "硬座"
    },
    {
        "index": 26,
        "name": "no_seat",
        "verbose": "无座",
        "display": False
    }
]

APPEND_MAPPING = [{"name": v["name"].replace("_code", ""),
                   "verbose": v["verbose"].replace("代码", ""),
                   "index": v["index"]} for v in TRAIN_MAPPING if
                  v["name"].endswith("_code")]
APPEND_PROPERTYS = [v["name"] for v in APPEND_MAPPING]
TRAINDETAIL_PROPERTYS = [v["name"] for v in TRAIN_MAPPING] + APPEND_PROPERTYS


class TrainProperty(object):
    __slots__ = ("name", "verbose", "value", "display")

    def __init__(self, data):
        for v in self.__slots__:
            setattr(self, v, data.get(v, True))

    def __str__(self):
        return str(type(self)) + ' '.join([
            "{attr}:{val}".format(attr=v, val=getattr(self, v)) for v in self.__slots__])

    __repr__ = __str__


class TrainDetail(object):
    __slots__ = tuple(TRAINDETAIL_PROPERTYS)

    def __init__(self, data):
        for v in TRAIN_MAPPING:
            setattr(self, v["name"],
                    TrainProperty(data={"name": v["name"],
                                        "verbose": v["verbose"],
                                        "display": v.get("display", True),
                                        "value": data[v["index"]]}))
        from pre_processing.cities import CityData
        for v in APPEND_MAPPING:
            setattr(self, v["name"],
                    TrainProperty(data={"name": v["name"],
                                        "verbose": v["verbose"],
                                        "display": v.get("display", True),
                                        "value": CityData.find_city_by_code(data[v["index"]])}))


class PassengerDetail(BasicMapping):
    # 删除 index_id
    __slots__ = ("passenger_name", "code", "sex_code", "sex_name",
                 "born_date", "country_code", "passenger_id_type_code",
                 "passenger_id_type_name", "passenger_id_no",
                 "passenger_type", "passenger_flag",
                 "passenger_type_name", "mobile_no", "phone_no",
                 "email", "address", "postalcode", "first_letter",
                 "recordCount", "total_times"
                 )


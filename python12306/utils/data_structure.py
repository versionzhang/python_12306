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

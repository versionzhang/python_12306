import re

import requests
from cached_property import cached_property

from python12306.comonexception import ResponseError
from python12306.utils.data_structure import CityStationMapping
from python12306.utils.log import Log

STATION_URL = "https://kyfw.12306.cn/otn/resources/js/framework/station_name.js"

city_re = re.compile("var station_names =\'(.*)\';")


class CityTool(object):

    def __init__(self):
        self.citydata = []

    @cached_property
    def raw_data(self):
        count = 10
        while count:
            try:
                r = requests.get(STATION_URL)
                if r.status_code == requests.codes.ok:
                    raw_data = city_re.findall(r.text)
                    if raw_data:
                        # remove empty line data.
                        data = map(lambda x: x.strip(), raw_data[0].split("@"))
                        Log.v("获取车站信息成功")
                        return list(filter(lambda x: bool(x), data))
                else:
                    count -= 1
                    Log.w("无法读取车站信息，重试中")
                    continue
            except requests.RequestException:
                count -= 1
                Log.w("获取车站信息失败，重试获取中")
                continue
        if count <= 0:
            raise ResponseError

    def to_python(self):
        data = self.raw_data
        self.citydata = [CityStationMapping(
            data=dict(zip((
                "abbr3",
                "name",
                "code",
                "pinyin",
                "abbr2",
                "num"
            ), v.split('|')))
        ) for v in data]
        return self

    def find_city_by_name(self, name):
        data = list(filter(lambda x: x.name == name, self.citydata))
        if data:
            return data[0]
        else:
            return None

    def find_city_by_code(self, code):
        data = list(filter(lambda x: x.code == code, self.citydata))
        if data:
            return data[0]
        else:
            return None

    def get_final_data(self):
        self.to_python()
        return self


CityData = CityTool().get_final_data()

import os
import pickle
import re
import datetime

import requests

from utils.data_structure import CityStationMapping

STATION_URL = "https://kyfw.12306.cn/otn/resources/js/framework/station_name.js"

city_re = re.compile("var station_names =\'(.*)\';")

class CityTool(object):

    def __init__(self):
        self.current = datetime.datetime.now()
        self.citydata = []

    def is_exists_pickle(self):
        return os.path.exists(self.pickle_path)

    @property
    def pickle_path(self):
        return os.path.join(
            os.path.abspath(os.path.dirname(__file__)),
            'citydata.pickle')

    def export_pickle(self):
        self.to_python()
        with open(os.path.join(self.pickle_path), 'wb') as handle:
            pickle.dump(self, handle)

    def load_exists_data(self):
        if self.is_exists_pickle():
            with open(os.path.join(self.pickle_path), 'rb') as handle:
                b = pickle.load(handle)
            # use modify time
            b.current = datetime.datetime.fromtimestamp(os.path.getmtime(self.pickle_path))
            return b

    @staticmethod
    def raw_data():
        r = requests.get(STATION_URL)
        if r.status_code == requests.codes.ok:
            raw_data = city_re.findall(r.text)
            if raw_data:
                # remove empty line data.
                data = map(lambda x: x.strip(), raw_data[0].split("@"))
                return list(filter(lambda x: bool(x), data))
        return []

    def to_python(self):
        data = self.raw_data()
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
        d = self.load_exists_data()
        if d:
            if d.current + datetime.timedelta(days=10) > self.current:
                return d
        self.export_pickle()
        return self


CityData = CityTool().get_final_data()

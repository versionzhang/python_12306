import os
import datetime
import pickle

from utils.data_structure import PassengerDetail


class PassengerTool(object):

    def __init__(self, raw_data):
        self.current = datetime.datetime.now()
        self.passenger = []
        self.raw_data = raw_data

    def is_exists_pickle(self):
        return os.path.exists(self.pickle_path)

    @property
    def pickle_path(self):
        return os.path.join(
            os.path.abspath(os.path.dirname(__file__)),
            'passengers.pickle')

    def export_pickle(self):
        self.to_python()
        with open(os.path.join(self.pickle_path), 'wb') as handle:
            pickle.dump(self, handle)

    def to_python(self):
        self.passenger = [PassengerDetail(v) for v in self.raw_data]
        return self


    def load_exists_data(self):
        if self.is_exists_pickle():
            with open(os.path.join(self.pickle_path), 'rb') as handle:
                b = pickle.load(handle)
            # use modify time
            b.current = datetime.datetime.fromtimestamp(os.path.getmtime(self.pickle_path))
            return b

    def find_people_by_names(self, names):
        data = list(filter(lambda x: x.name in names, self.passenger))
        return data

    def get_final_data(self):
        d = self.load_exists_data()
        if d:
            # 两个小时的有效期
            if d.current + datetime.timedelta(hours=2) > self.current:
                return d
        self.export_pickle()
        return self


PassengerData = PassengerTool(raw_data=[]).get_final_data()

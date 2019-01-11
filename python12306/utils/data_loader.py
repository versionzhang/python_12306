import os
import datetime
import pickle


class LocalSimpleCache(object):

    def __init__(self, raw_data, pickle_name, expire_time=2):
        """
        :param raw_data: 需要导出的数据
        :param pickle_name: 导出的pickle名称
        :param expire_time: 过期时间, 单位小时
        """
        self.current = datetime.datetime.now()
        self.pickle_name = pickle_name
        self.raw_data = raw_data
        self.expire_time = expire_time

    def is_exists_pickle(self):
        return os.path.exists(self.pickle_path)

    @property
    def pickle_path(self):
        return os.path.join(
            os.path.abspath(os.path.dirname(__file__)),
            self.pickle_name)

    def export_pickle(self):
        with open(os.path.join(self.pickle_path), 'wb') as handle:
            pickle.dump(self, handle)

    def load_exists_data(self):
        if self.is_exists_pickle():
            with open(os.path.join(self.pickle_path), 'rb') as handle:
                b = pickle.load(handle)
            # use modify time
            b.current = datetime.datetime.fromtimestamp(os.path.getmtime(self.pickle_path))
            return b

    def get_final_data(self):
        d = self.load_exists_data()
        if d and d.raw_data:
            # 两个小时的有效期
            if d.current + datetime.timedelta(hours=self.expire_time) > self.current:
                return d
        self.export_pickle()
        return self

import pickle
import time

import redis

from global_data.const_data import find_by_name
from global_data.session import LOGIN_SESSION
from logic.login.login import NormalLogin
from logic.query.query import Query
from config import Config
from logic.submit.submit import NormalSubmitDcOrder
from utils.log import Log
from utils.data_loader import LocalSimpleCache

server = redis.Redis()

class Schedule(object):
    retry_login_time = Config.basic_config.retry_login_time
    login_status = False

    def run(self):
        s = LocalSimpleCache('', 'logincookie.pickle').get_final_data()
        if not s.raw_data:
            while True:
                l = NormalLogin()
                status, _ = l.login()
                if not status:
                    Log.v("")
                    return
                else:
                    Log.v("导出已经登录的cookie")
                    s.raw_data = LOGIN_SESSION.cookies
                    s.export_pickle()
                    break
        else:
            Log.v("加载已经登录的cookie")
            LOGIN_SESSION.cookies.update(s.raw_data)
        while True:
            q = Query()
            data = q.filter()
            for v in data:
                print(v[0])
                q.pretty_output(v[1])
            time.sleep(5)
            for v in data:
                submit = NormalSubmitDcOrder(v[1], v[0])
                f = submit.run()
                if not f:
                    continue
                else:
                    break

if __name__ == "__main__":
    s = Schedule()
    s.run()

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
        s = LocalSimpleCache('', 'logincookie.pk').get_final_data()
        if not s.raw_data:
            l = NormalLogin()
            status, _ = l.login()
            if not status:
                return
            else:
                Log.v("导出已经登录的cookie")
                s.raw_data = LOGIN_SESSION.cookies
                s.export_pickle()
        else:
            Log.v("加载已经登录的cookie")
            LOGIN_SESSION.cookies.update(s.raw_data)

        q = Query()
        data = q.filter()
        time.sleep(5)
        seat_code = find_by_name('seat', Config.basic_config.ticket_types[0]).sys_code
        submit = NormalSubmitDcOrder(data, seat_code)
        submit.run()

if __name__ == "__main__":
    s = Schedule()
    s.run()

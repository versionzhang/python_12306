import time

from global_data.session import LOGIN_SESSION
from logic.login.login import NormalLogin
from logic.query.query import Query
from config import Config
from logic.submit.fastsubmit import FastSubmitDcOrder
from logic.submit.submit import NormalSubmitDcOrder
from utils.log import Log
from utils.data_loader import LocalSimpleCache


class Schedule(object):
    retry_login_time = Config.basic_config.retry_login_time
    login_status = False

    def run(self):
        s = LocalSimpleCache('', 'logincookie.pickle').get_final_data()
        if not s.raw_data:
            while self.retry_login_time:
                l = NormalLogin()
                status, msg = l.login()
                if not status:
                    Log.v("登录失败, 重试中")
                    self.retry_login_time -= 1
                    continue
                else:
                    Log.v("导出已经登录的cookie")
                    s.raw_data = LOGIN_SESSION.cookies
                    s.export_pickle()
                    break
            if not self.retry_login_time:
                Log.v("重试次数已经超过设置")
                return
        else:
            Log.v("加载已经登录的cookie")
            LOGIN_SESSION.cookies.update(s.raw_data)
        while True:
            q = Query()
            data = q.filter()
            if not data:
                Log.v("未查到满足条件的车次")
            for v in data:
                print(v[0])
                q.pretty_output(v[1])
            time.sleep(5)
            for v in data:
                submit = FastSubmitDcOrder(v[1], v[0])
                f = submit.run()
                if not f:
                    continue
                else:
                    break


if __name__ == "__main__":
    instance = Schedule()
    instance.run()

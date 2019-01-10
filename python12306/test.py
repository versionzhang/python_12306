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
            count = 0
            while self.retry_login_time:
                l = NormalLogin()
                Log.v("正在为您登录")
                status, msg = l.login()
                if not status:
                    count += 1
                    Log.v("登录失败, 重试{0}次".format(count))
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
        Log.v("正在查询车次余票信息")
        count = 0
        while True:
            count += 1
            q = Query()
            data = q.filter()
            if not data:
                Log.v("满足条件的车次暂无余票,正在重新查询")
            for v in data:
                print(v[0])
                q.pretty_output(v[1])
            time.sleep(5)
            Log.v("查询{0}次".format(count))
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

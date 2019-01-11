import datetime
import random
import time

from global_data.session import LOGIN_SESSION
from logic.login.login import NormalLogin
from logic.query.query import Query
from config import Config
from logic.submit.fastsubmit import FastSubmitDcOrder
from logic.submit.submit import NormalSubmitDcOrder
from utils.send_email import send_email
from utils.log import Log
from utils.data_loader import LocalSimpleCache


class Schedule(object):
    retry_login_time = Config.basic_config.retry_login_time
    login_status = False
    order_id = ''

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
                    Log.v("登录成功")
                    Log.v("导出已经登录的cookie,已便下次使用")
                    Log.v("cookie的有效期为 {0}小时".format(s.expire_time))
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
            n = datetime.datetime.now()
            q = Query()
            data = q.filter()
            if not data:
                Log.v("满足条件的车次暂无余票,正在重新查询")
            for v in data:
                print("当前座位席别 {}".format(v[0].name))
                q.pretty_output(v[1])
            delta_time = datetime.datetime.now() - n
            try:
                delta = Config.basic_config.query_left_ticket_time - 1 + random.random()
            except AttributeError:
                delta = 4 + random.random()
            time.sleep(delta)
            Log.v("查询第 {0} 次, 当次查询时间间隔为 {1} 秒, 查询请求处理时间 {2} 秒".format(
                count, delta, delta_time.total_seconds()))
            for v in data:
                if Config.basic_config.fast_submit:
                    submit = FastSubmitDcOrder(v[1], v[0])
                else:
                    submit = NormalSubmitDcOrder(v[1], v[0])
                f = submit.run()
                if not f:
                    continue
                else:
                    self.order_id = submit.order_id
                    break
            if self.order_id:
                break

        Log.v("抢票成功，如果有配置邮箱，稍后会收到邮件通知")
        # 抢票成功发邮件信息
        send_email(2, **{"order_no": self.order_id})

if __name__ == "__main__":
    instance = Schedule()
    instance.run()

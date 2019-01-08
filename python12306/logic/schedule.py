import time
from logic.login.login import NormalLogin
from logic.query.query import Query
from config import Config
from utils.log import Log


class Schedule(object):
    retry_login_time = Config.basic_config.retry_login_time
    login_status = False

    def run(self):
        while self.retry_login_time:
            l = NormalLogin()
            result, msg = l.login()
            if not result:
                Log.e("登录失败, 重试中")
                self.retry_login_time-=1
            else:
                self.login_status = True
                break
        if not self.login_status:
            Log.e("登录失败, 可重启路由或等待一段时间重试")


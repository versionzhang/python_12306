import datetime
import time
from queue import Queue
from multiprocessing.pool import ThreadPool

from python12306.config import Config

from python12306.logic.query.dispatcher import DispatcherTool
from python12306.scheduler import Schedule as BaseSchedule


class Schedule(BaseSchedule):
    retry_login_time = Config.basic_config.retry_login_time
    order_id = ''
    order_tickets = []
    pool = ThreadPool(5)

    def batch_tasks(self, query_date):
        n = datetime.datetime.now()
        data = DispatcherTool.run(query_date)
        self.submit_order(data)
        if self.order_id:
            self.pool.close()
        DispatcherTool.output_delta_time(n)

    def run(self):
        self.pre_check()
        while True:
            self.maintain_mode()
            self.heart_beat_mode()

            dates = DispatcherTool.query_travel_dates
            self.pool.map(self.batch_tasks, dates)
            self.pool.close()
            if self.order_id or self.unfinished_order:
                break
        self.notice_user()


if __name__ == "__main__":
    instance = Schedule()
    instance.run()

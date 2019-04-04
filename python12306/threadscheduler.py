import datetime
from itertools import product
from multiprocessing.pool import ThreadPool

from python12306.config import Config

from python12306.logic.query.dispatcher import DispatcherTool
from python12306.scheduler import Schedule as BaseSchedule


class Schedule(BaseSchedule):
    retry_login_time = Config.basic_config.retry_login_time
    order_id = ''
    order_tickets = []
    pool = ThreadPool(5)

    def batch_tasks(self, query_data):
        n = datetime.datetime.now()
        data = DispatcherTool.run(query_data)
        DispatcherTool.output_delta_time(n)
        self.submit_order(data)
        if self.order_id:
            self.pool.close()

    def run(self):
        self.maintain_mode()
        self.pre_check()
        while True:
            self.maintain_mode()
            self.heart_beat_mode()

            dates = DispatcherTool.query_travel_dates
            if Config.basic_config.use_station_group:
                station_groups = [(v.from_station, v.to_station) for v in Config.basic_config.station_groups]
            else:
                station_groups = list(product(Config.basic_config.from_stations, Config.basic_config.to_stations))
            query_params = list(product(dates, station_groups))

            self.pool.map(self.batch_tasks, query_params)
            if self.order_id or self.unfinished_order:
                self.pool.close()
                break
        self.notice_user()


if __name__ == "__main__":
    instance = Schedule()
    instance.run()

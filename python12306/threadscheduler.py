import datetime
import time
from queue import Queue
from threading import Thread

from python12306.config import Config

from python12306.logic.login.checkuser import OnlineCheckerTool
from python12306.logic.login.login import NormalLogin
from python12306.logic.login.passager import QueryPassengerTool
from python12306.logic.query.dispatcher import DispatcherTool
from python12306.logic.submit.fastsubmit import FastSubmitDcOrder
from python12306.logic.submit.submit import NormalSubmitDcOrder

from python12306.scheduler import Schedule as BaseSchedule

from python12306.utils.send_email import send_email
from python12306.utils.log import Log


class Worker(Thread):
    """ Thread executing tasks from a given tasks queue """

    def __init__(self, tasks):
        Thread.__init__(self)
        self.tasks = tasks
        self.daemon = True
        self.start()

    def run(self):
        while True:
            func, args, kargs = self.tasks.get()
            try:
                func(*args, **kargs)
            except Exception as e:
                # An exception happened in this thread
                print(e)
            finally:
                # Mark this task as done, whether an exception happened or not
                self.tasks.task_done()


class ThreadPool(object):
    """ Pool of threads consuming tasks from a queue """

    def __init__(self, num_threads):
        self.tasks = Queue(num_threads)
        for _ in range(num_threads):
            Worker(self.tasks)

    def add_task(self, func, *args, **kargs):
        """ Add a task to the queue """
        self.tasks.put((func, args, kargs))

    def map(self, func, args_list):
        """ Add a list of tasks to the queue """
        for args in args_list:
            self.add_task(func, args)

    def wait_completion(self):
        """ Wait for completion of all the tasks in the queue """
        self.tasks.join()


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
            self.pool.wait_completion()
            if self.order_id or self.unfinished_order:
                break
        self.notice_user()


if __name__ == "__main__":
    instance = Schedule()
    instance.run()

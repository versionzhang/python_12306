from python12306.scheduler import Schedule
from python12306.threadscheduler import Schedule as Multischedule
from python12306.config import Config


def main():
    instance = Multischedule() if Config.multi_threading_enable else Schedule()
    instance.run()


if __name__ == "__main__":
    main()

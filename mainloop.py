import sys

from python12306.scheduler import Schedule
from python12306.threadscheduler import Schedule as Multischedule


def main(mode):
    instance = Multischedule() if mode == "multi" else Schedule()
    instance.run()


if __name__ == "__main__":
    cmd = sys.argv[1].lower() if sys.argv[1:] else ''
    main(cmd)

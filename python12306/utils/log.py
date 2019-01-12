import os
import datetime
import logging.handlers

from colorama import Fore

from config import Config

logger = logging.getLogger()
ticket_logger = logging.getLogger('ticket')
ticket_logger.setLevel(logging.DEBUG)
formatter = logging.Formatter(
    '[%(asctime)s] %(levelname)s - %(message)s', '%Y-%m-%d %H:%M:%S'
)

# Add the log message handler to the logger
handler = logging.handlers.RotatingFileHandler(
    os.path.join(os.path.abspath(os.path.dirname(__file__)),
                 '../logs/buy_ticket-{0}.log'.format(
                     datetime.datetime.now().strftime("%Y-%m-%d-%H-%M"))),
    maxBytes=20 * 1024 * 1024, backupCount=5)
handler.setFormatter(formatter)
ticket_logger.addHandler(handler)


class LogUtils(object):

    @staticmethod
    def __print(msg, msg_type):
        """
        :param msg: log text.
        :param color: [Fore.GREEN, Fore.BLUE, Fore.YELLOW, Fore.RED]
        :param msg_type: [info, debug, warning, error]
        :return:
        """
        maping = dict(info=Fore.GREEN, debug=Fore.BLUE, warning=Fore.YELLOW, error=Fore.RED)
        l = getattr(ticket_logger, msg_type)
        if type(msg) == str:
            if Config.basic_config.debug or msg_type != 'debug':
                print("\t\t\t" +maping[msg_type] + msg + Fore.RESET)
            l(msg)
        else:
            if Config.basic_config.debug or msg_type != 'debug':
                print(maping[msg_type])
                print(msg)
                print(Fore.RESET)
            l(msg)

    def d(self, msg):
        # debug msg
        self.__print(msg, 'debug')

    def v(self, msg):
        # verbose msg
        self.__print(msg, 'info')

    def w(self, msg):
        # warning msg
        self.__print(msg, 'warning')

    def e(self, msg):
        # error msg
        self.__print(msg, 'error')


Log = LogUtils()

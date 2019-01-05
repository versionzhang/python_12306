from colorama import Fore


class LogUtils(object):

    @staticmethod
    def __print(msg, color):
        if type(msg) == str:
            print(color + msg + Fore.RESET)
        else:
            print(color)
            print(msg)
            print(Fore.RESET)

    def d(self, msg):
        # debug msg
        self.__print(msg, Fore.BLUE)

    def v(self, msg):
        # verbose msg
        self.__print(msg, Fore.GREEN)

    def w(self, msg):
        # warning msg
        self.__print(msg, Fore.YELLOW)

    def e(self, msg):
        # error msg
        self.__print(msg, Fore.RED)

Log = LogUtils()

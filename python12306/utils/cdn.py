import copy
import math
import random
import socket
import time
from multiprocessing.pool import ThreadPool
from threading import Lock

import requests
from python12306.utils.data_loader import LocalSimpleCache

from python12306.utils.log import Log
from urllib3.exceptions import SSLError, MaxRetryError

from python12306.global_data.useragent import CHROME_USER_AGENT
from python12306.resources.cdn_list import CDN_LIST
from python12306.utils.data_structure import CDNRecord


headers = {
            'Host': r'kyfw.12306.cn',
            'Referer': 'https://kyfw.12306.cn/otn/login/init',
            'User-Agent': CHROME_USER_AGENT,
}


class CdnChecker(object):
    def __init__(self):
        self.raw_cdn_list = copy.copy(CDN_LIST)
        self.result = []
        self.status = False
        self.pool = ThreadPool(10)
        self.lock = Lock()
        self.max_available_level = 5

    @property
    def check_url(self):
        return "/otn/login/init"

    def build_url(self, cdn_ip):
        return "http://{0}/{1}".format(cdn_ip, self.check_url)

    def update_result(self, result):
        with self.lock:
            if not any(filter(lambda x: x.ip == result.ip, self.result)):
                self.result.append(result)
            else:
                for i, v in enumerate(self.result):
                    if v.ip == result["ip"]:
                        # update level
                        self.result[i].level = math.ceil((self.result[i].level + result.level) / 2)

    def remove_ip(self, ip):
        with self.lock:
            # remove ip in result
            data = list(filter(lambda x: x.ip != ip, self.result))
            self.result = data

    def verify(self, cdn_ip):
        """
        level: 0:
        :param cdn_ip: ip address
        :return:
        """
        start = time.time()
        try:
            response = requests.get(self.build_url(cdn_ip), headers=headers, timeout=6)
            end = time.time()
            if response.status_code == requests.codes.ok and 'message' not in response.text:
                delta = end - start
                result = CDNRecord(dict(ip=cdn_ip, level=math.ceil(delta/0.5)))
                self.update_result(result)
                return True
        except (requests.exceptions.Timeout, requests.exceptions.ReadTimeout, requests.exceptions.ConnectionError):
            pass
        except socket.error:
            pass
        except (SSLError, MaxRetryError):
            pass
        self.remove_ip(cdn_ip)
        return False

    def run(self):
        Log.v("您已开启cdn加速")
        Log.v("正在检查cdn列表可用状态....(大概将会花费10分钟左右)")
        self.pool.map(self.verify, self.raw_cdn_list)
        self.status = True
        Log.v("共获取{0}个可用的cdn".format(len(self.result)))
        Log.v("各个cdn的等级情况如下(level等级越低证明, cdn的连接更快):")
        level_result = [v.level for v in self.result]
        level_types = set(level_result)
        for v in level_types:
            Log.v("level {0} 共有 {1} 个".format(v, level_result.count(v)))

    def choose_one(self):
        return random.choice([v for v in self.result if v.level <= self.max_available_level])

    def load_exists(self):
        s = LocalSimpleCache([], "cdn.pickle", expire_time=24)
        load = s.get_final_data()
        if not load.raw_data:
            self.run()
            s.raw_data = self.result
            Log.v("导出已经检查完毕的cdn列表")
            s.export_pickle()
        else:
            Log.v("您已开启cdn加速")
            Log.v("正在导入之前检查的cdn列表")
            self.status = True
            self.result = load.raw_data
            Log.v("共导入{0}个可用的cdn".format(len(self.result)))
            Log.v("各个cdn的等级情况如下(level等级越低证明, cdn的连接更快):")
            level_result = [v.level for v in self.result]
            level_types = set(level_result)
            for v in level_types:
                Log.v("level {0} 共有 {1} 个".format(v, level_result.count(v)))
        return self


CdnStorage = CdnChecker()

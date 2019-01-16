import copy
import math
import socket
import time

import requests
from urllib3.exceptions import SSLError, MaxRetryError

from python12306.global_data.useragent import CHROME_USER_AGENT
from python12306.resources.cdn_list import CDN_LIST
from python12306.utils.data_structure import CDNRecord


headers = {
            'Host': r'kyfw.12306.cn',
            'Referer': 'https://kyfw.12306.cn/otn/login/init',
            'User-Agent': CHROME_USER_AGENT,
        }


class CdnTools(object):
    def __init__(self):
        self.raw_cdn_list = copy.copy(CDN_LIST)
        self.result = []

    @property
    def check_url(self):
        return "/otn/login/init"

    def build_url(self, cdn_ip):
        return "http://{0}/{1}".format(cdn_ip, self.check_url)

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
                self.result.append(result)
                return True
            return False
        except (requests.exceptions.Timeout, requests.exceptions.ReadTimeout, requests.exceptions.ConnectionError):
            return False
        except socket.error:
            return False
        except (SSLError, MaxRetryError):
            return False




import copy

from python12306.resources.cdn_list import CDN_LIST
from python12306.utils.data_structure import CDNRecord

class CdnTools(object):
    def __init__(self):
        self.raw_cdn_list = copy.copy(CDN_LIST)
        self.result = []

    def verify(self, cdn_ip):
        """
        level: 0:
        :param cdn_ip: ip address
        :return:
        """


# -*- coding: UTF-8 -*-

from scrapy import cmdline
import requests
import time
import threading
import logging
from drug.settings import IPPOOL
import random

logger = logging.getLogger(__name__)


# 获取代理IP的线程类
class GetIpThread(threading.Thread):
    def __init__(self, api_url, fetch_second):
        super(GetIpThread, self).__init__()
        self.fetchSecond = fetch_second
        self.apiUrl = api_url

    def run(self):
        while True:
            # 获取IP列表
            res = requests.get(self.apiUrl).content.decode()
            # 按照\n分割获取到的IP
            for ip in res.split('\n'):
                IPPOOL.append(ip)
            logging.warn("ipPool:   " + IPPOOL)
            # 休眠
            time.sleep(self.fetchSecond)



if __name__ == '__main__':
    # # 这里请填写你在无忧代理IP的API接口，接口返回格式为TXT，分隔符为\n
    # apiUrl = "http://api.ip.data5u.com/dynamic/get.html?order=【把这里换成你的IP提取码】&sep=3"
    # # 获取IP时间间隔，建议为5秒
    # fetchSecond = 5
    # # 开始自动获取IP
    # GetIpThread(apiUrl, fetchSecond).start()


    # 开始爬数据
    cmdline.execute("scrapy crawl 39drug".split())



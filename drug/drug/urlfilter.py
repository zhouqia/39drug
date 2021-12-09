import os

from scrapy.dupefilters import BaseDupeFilter
import logging

class BlogDupeFilter(BaseDupeFilter):
    """
    自定义一个url去重的类
    """
    def __init__(self):
        self.vistited_urls = set()

    @classmethod
    def from_settings(cls, settings):
        return cls()

    def request_seen(self, request):
        # print('当前的request', request)
        """
        简单粗暴的将当前的url添加到set集合上,
        当当前的url存在于set集合里面,那么就返回True
        如果不存在就添加到set集合
        """
        if request.url in self.vistited_urls:
            print('重复请求', request)
            logging.warn('重复请求 ' + request.url)
            return True
        self.vistited_urls.add(request.url)
        return False
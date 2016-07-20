# coding:utf8

"""
URLFetcher.py
~~~~~~~~~~~~~

该模块用于下载网页源代码, 允许自定义header与使用代理服务器
"""

from datetime import datetime
import logging
import re
import requests
import time
import traceback

log = logging.getLogger('Main.URLFetcher')


class URLFetcher(object):

    def __init__(self, url):
        self.url = url
        self.page_source = None
        self.response_headers = None
        self.request_time = None
        self.response_time = None
        self.headers = None
        self.status_code = None
        self.customize_headers()

    def fetch(self, retry=2, proxies=None):
        '''获取html源代码'''
        try:
            # prefetch is invalid now of requests 2.7.
            self.request_time = datetime.now()
            response = requests.get(self.url, headers=self.headers,
                                    timeout=10, proxies=proxies)

            if self._is_response_available(response):
                self.response_time = datetime.now()
                self.handle_encoding(response)
                self.page_source = response.text
                self.response_headers = response.headers
                self.status_code = response.status_code
                return True
            else:
                log.warning('Page not available. Status code:%d URL: %s \n' % (
                    response.status_code, self.url))
        except Exception, e:
            if retry > 0:  # 超时重试
                return self.fetch(retry - 1)
            else:
                log.debug(str(e) + ' URL: %s \n' % self.url)
        return None

    def customize_headers(self, **kargs):
        # 自定义header,防止被禁,某些情况如豆瓣,还需制定cookies,否则被ban
        # 使用参数传入可以覆盖默认值，或添加新参数，如cookies
        self.headers = {
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'Accept-Charset': 'gb18030,utf-8;q=0.7,*;q=0.3',
            'Accept-Encoding': 'gzip,deflate,sdch',
            'Accept-Language': 'en-US,en;q=0.8',
            'Connection': 'keep-alive',
            # 设置Host会导致TooManyRedirects, 因为hostname不会随着原url跳转而更改,可不设置
            # 'Host':urlparse(self.url).hostname
            'User-Agent': 'Mozilla/5.0 (X11; Linux i686) AppleWebKit/537.4 (KHTML, like Gecko) Chrome/22.0.1229.79 Safari/537.4',
            'Referer': self.url,
        }
        self.headers.update(kargs)

    def get_data(self):
        return self.url, self.page_source

    def get_response_headers(self):
        return self.response_headers

    def _is_response_available(self, response):
        return True if response.status_code == requests.codes.ok else False

    def handle_encoding(self, response):
        # requests会自动处理编码问题.
        # 但是当header没有指定charset并且content-type包含text时,
        # 会使用RFC2616标准，指定编码为ISO-8859-1
        # 因此需要用网页源码meta标签中的charset去判断编码
        if response.encoding == 'ISO-8859-1':
            charset_re = re.compile("((^|;)\s*charset\s*=)([^\"']*)", re.M)
            charset = charset_re.search(response.text)
            charset = charset and charset.group(3) or None
            response.encoding = charset

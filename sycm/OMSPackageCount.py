# -*- coding: UTF-8 -*-
'''
@author: Andrewzhj
@contact: andrew_zhj@126.com
@file: OMSPackageCount.py
@time: 2018/9/26 16:57
@desc:
@note:
'''
import json
import sys
sys.path.append("../")
import pymysql
import urllib.parse
import urllib.request
import http.cookiejar

from sycm import Config as config



params = {
    'loginCustomerId': '',
    'partnerCode': "GTBU",
    'password': "cbc8f5435c87e13c5d14e6ce92358d68",
    'streamNo': "web_bss1537955116557745223",
    'userCode': "zhengjiang"
}

query = {
    'appid': "6074c6aa3488f3c2dddff2a7ca821aab",
    'currentPage': 1,
    'endDate': '1539100800000',
    'loginCustomerId': "6074c6aa3488f3c2dddff2a7ca821aab",
    'partnerCode': "GTBU",
    'perPageCount': 10,
    'sign': "ceae715b68823ad87f7ff093a01d1969",
    'startDate': 1537804800000,
    'streamNo': "web_bss1538044313738392887",
    'timestamp': 1538044313738,
}

class OMSPackageCount(object):
    def __init__(self):
        self._db = pymysql.connect(config.DB_HOST, config.DB_USER, config.DB_PWD, config.DB_NAME, charset=config.DB_CHARSET)
        self._cursor = self._db.cursor()
        self._user = config.OMS_LOGIN_USER
        self._header = config.OMS_HEADER

    def fetchCookie(self):
        url = "https://order.roamingman.com.cn/oms/loginforoms/login"
        data = json.dumps(params)
        data = bytes(data, 'utf8')
        # req = urllib.request.Request(url, headers=self._header)
        # result = urllib.request.urlopen(req, data).read().decode('utf-8')
        # print(result)

        cookie_filename = 'cookie.txt'
        cookie = http.cookiejar.MozillaCookieJar(cookie_filename)
        req = urllib.request.Request(url, headers=self._header)
        result = urllib.request.urlopen(req, data).read().decode('utf-8')
        print(result)
        cookie.save(ignore_discard=True, ignore_expires=True)

        handler = urllib.request.HTTPCookieProcessor(cookie)
        opener = urllib.request.build_opener(handler)
        _package_count_url = "https://order.roamingman.com.cn/oms/package/packageCount"
        query_data = json.dumps(query)
        query_data = bytes(query_data, 'utf8')
        _request = urllib.request.Request(_package_count_url, headers=self._header)
        response = opener.open(_request).read().decode('utf-8')
        # _req = urllib.request.Request(_package_count_url, headers=self._header)
        # _result = urllib.request.urlopen(_req, query_data).read().decode('utf-8')
        print(response)



if __name__ == '__main__':
    oms = OMSPackageCount()
    oms.fetchCookie()

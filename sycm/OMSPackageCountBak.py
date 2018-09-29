# -*- coding: UTF-8 -*-
'''
@author: Andrewzhj
@contact: andrew_zhj@126.com
@file: OMSPackageCountBak.py
@time: 2018/9/29 15:03
@desc:
@note:
'''
import json
import urllib.parse
import urllib.request
import http.cookiejar

params = {
    'loginCustomerId': '',
    'partnerCode': "GTBU",
    'password': "cbc8f5435c87e13c5d14e6ce92358d68",
    'streamNo': "web_bss1537955116557745223",
    'userCode': "zhengjiang"
}

cj = http.cookiejar.CookieJar()

cookie = urllib.request.HTTPCookieProcessor(cj)
opener = urllib.request.build_opener(cookie)

query_data = json.dumps(params)
query_data = bytes(query_data, 'utf8')

response = opener.open("https://order.roamingman.com.cn/oms/loginforoms/login", data=query_data)

print(response)
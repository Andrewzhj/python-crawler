# -*- coding: UTF-8 -*-
'''
@author: Andrewzhj
@contact: andrew_zhj@126.com
@file: Common.py
@time: 2018/10/15 16:29
@desc:
@note:
'''

import requests
session = requests.Session()

class Common(object):
    def __init__(self):
        pass

    @staticmethod
    def getRequestSession():
        return session
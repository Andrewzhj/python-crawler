# -*- coding: UTF-8 -*-
'''
@author: Andrewzhj
@contact: andrew_zhj@126.com
@file: Application.py
@time: 2018/8/31 15:11
@desc:
@note:
'''

import sys
sys.path.append("../")

from sycm.Common import Common
from sycm.HotItemTrend import HotItemTrend
from sycm.HotItem import HotItem
from sycm.PackageGroup import PackageGroup
from sycm.Producer import Producer

class Application(object):

    def __init__(self):
        self._hotItemTrend = HotItemTrend()
        self._hotItem = HotItem()
        self._packageGroup = PackageGroup()
        self._producer = Producer()

    def fetchHotItemTrend(self, saturday_date):
        self._hotItemTrend.start(saturday_date)

    def fetchHotItem(self):
        self._hotItem.start()

    def packageGroup(self):
        self._packageGroup.group()

    def fillProducer(self):
        self._producer.start()

if __name__ == '__main__':
    app = Application()

    # 抓取热销商品信息，必须先执行。热销商品趋势是根据热销商品数据调用接口获取的
    app.fetchHotItem()

    # 每周六爬取上周的商品趋势信息。
    # last_saturday_date = Common.get_date_time('2018-09-08')
    last_saturday_date = Common.get_last_saturday()
    app.fetchHotItemTrend(last_saturday_date)

    # 数据充实商品供应商、根据商品标题执行套餐分组
    app.fillProducer()
    app.packageGroup()

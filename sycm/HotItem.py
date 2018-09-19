# -*- coding: UTF-8 -*-
'''
@author: Andrewzhj
@contact: andrew_zhj@126.com
@file: HotItem.py
@time: 2018/8/30 18:08
@desc:
@note:
'''
import sys
sys.path.append("../")

import json
import math
import time
import urllib.parse
import urllib.request

import pymysql

from sycm import Config as config
from sycm.Common import Common


class HotItem(object):

    def __init__(self):
        self._user = config.LOGIN_USER
        self._header = config.HEADER
        self._db = pymysql.connect(config.DB_HOST, config.DB_USER, config.DB_PWD, config.DB_NAME, charset=config.DB_CHARSET)
        self._cursor = self._db.cursor()
        self._fetchDate = Common.get_fetch_date()

    def fetch(self, date_time):
        page = 1
        pageSize = 50
        totalPage = -1
        cmDate = Common.format_date(date_time)
        print("fetchHotSaleProduce cmDate: %s" % cmDate)
        while True:
            url = "https://sycm.taobao.com/mq/rank/listItems.json?cateId=124864009&categoryId=124864009&dateRange=" + cmDate + \
                  "%7C" + cmDate + "&dateRangePre=" + cmDate + "|" + cmDate + \
                  "&dateType=day&dateTypePre=day&device=0&devicePre=0&itemDetailType=1&keyword=&orderDirection=desc&orderField=payOrdCnt&page=" + \
                  str(page) + "&pageSize=" + str(
                pageSize) + "&rankTabIndex=0&rankType=1&seller=-1&token=0720623d1&view=rank&_=1534991498368"
            req_data = urllib.parse.urlencode(self._user).encode('utf-8')
            _req = urllib.request.Request(url, data = req_data, headers = self._header)
            with urllib.request.urlopen(_req) as response:
                _json = json.loads(response.read().decode('utf-8'))
                if totalPage == -1:
                    recordCount = _json['content']['data']['recordCount']
                    totalPage = int(math.ceil(recordCount / pageSize))
                print("------------------------------")
                print("fetchHotSaleProduce totalPage: %s, page: %s, recordCount: %s" %(totalPage, page, recordCount))
                data = _json['content']['data']['data']
                self.saveHotItem(data, cmDate)
            page += 1
            time.sleep(1)
            if page > totalPage:
                break

    def saveHotItem(self, data, cmDate):
        _sql = "INSERT INTO sycm_hot_sale_produce (itemTitle, itemId, shopName, tradeIndexCrc, payByrRateIndex, orderNum, payOrdCnt, itemPrice, cmDate, fetchDate) VALUES ('%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s')"
        for o in data:
            itemTitle = str(o['itemTitle'])
            itemId = str(o['itemId'])
            shopName = str(o['shopName'])
            tradeIndexCrc = 0
            try:
                tradeIndexCrc = o['tradeIndexCrc']
            except Exception as e:
                print("tradeIndexCrc Null")
            payByrRateIndex = 0
            try:
                payByrRateIndex = o['payByrRateIndex']
            except Exception as e:
                print("payByrRateIndex Null")
            orderNum = o['orderNum']
            payOrdCnt = o['payOrdCnt']
            itemPrice = o['itemPrice']
            try:
                sql = _sql % (itemTitle, itemId, shopName, str(tradeIndexCrc), str(payByrRateIndex), str(orderNum), str(payOrdCnt), str(itemPrice), cmDate, self._fetchDate)
                self.executeSQL(sql)
            except Exception as e:
                print("sql error: %s" % sql)

    def start(self):
        try:
            self.loopFetch()
        except Exception as e:
            print("Exception: %s" % (e))

    def loopFetch(self):
        current_date = Common.now_date_time()
        current_date = Common.last_day_date(current_date)
        while True:
            if self.ifHotSaleProduceNotExist(current_date):
                self.fetch(current_date)
                current_date = Common.last_day_date(current_date)
            else:
                return


    def executeSQL(self, sql):
        self._cursor.execute(sql)
        self._db.commit()

    def close(self):
        self._cursor.close()
        self._db.close()

    def ifHotSaleProduceNotExist(self, cm_date):
        sql = "SELECT COUNT(1) FROM sycm_hot_sale_produce WHERE cmDate='%s'" % Common.format_date(cm_date)
        self._cursor.execute(sql)
        rowCount = self._cursor.fetchone()
        return rowCount[0] == 0

if __name__ == '__main__':
    hotItem = HotItem()
    hotItem.start()
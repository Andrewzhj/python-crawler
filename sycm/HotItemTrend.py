# -*- coding: UTF-8 -*-
'''
@author: Andrewzhj
@contact: andrew_zhj@126.com
@file: HotItemTrend.py
@time: 2018/8/31 9:57
@desc:
@note:
'''
import sys
sys.path.append("../")

import datetime
import json
import math
import time
import urllib.parse
import urllib.request

import pymysql

from sycm import Config as config
from sycm.Common import Common

'''
爬取生意参谋热销商品信息
'''
class HotItemTrend(object):

    def __init__(self):
        self._user = config.LOGIN_USER
        self._header = config.HEADER
        self._db = pymysql.connect(config.DB_HOST, config.DB_USER, config.DB_PWD, config.DB_NAME, charset=config.DB_CHARSET)
        self._cursor = self._db.cursor()
        self._fetchDate = Common.get_fetch_date()

    def fetch(self, saturday_date):
        itemList = self.getItemList(saturday_date)
        for item in itemList:
            print("getItemIdList ItemId: %s" % str(item))
            itemId = str(item[0])
            itemTitle = str(item[1])
            shopName = str(item[2])
            cmDate = str(item[3])
            if not(self.ifItemTrendNotExist(itemId, cmDate)):
                continue
            url = "https://sycm.taobao.com/mq/rank/listItemTrend.json?cateId=124864009&categoryId=124864009&dateRange=" + cmDate + "%7C" + cmDate + "&dateRangePre=" + cmDate + "|" + cmDate + \
                  "&dateType=day&dateTypePre=day&device=0&devicePre=0&indexes=payOrdCnt,payByrRateIndex,payItemQty&itemDetailType=1&itemId=" + itemId + \
                  "&latitude=undefined&rankTabIndex=0&rankType=1&seller=-1&token=c72a36b5f&view=detail&_=1535090491291"
            req_data = urllib.parse.urlencode(self._user).encode('utf-8')
            _req = urllib.request.Request(url, data=req_data, headers=self._header)
            with urllib.request.urlopen(_req) as response:
                _json = json.loads(response.read().decode('utf-8'))
                try:
                    self.saveItemTrend(_json['content']['data'], itemTitle, itemId, shopName, saturday_date)
                except Exception as e:
                    print("Error! _json: %s, Exception: %s" % (_json, e))
                    itemTrendCode = str(_json['content']['code'])
                    _sql = "UPDATE sycm_hot_sale_produce SET itemTrendCode='%s' WHERE itemId='%s' AND cmDate='%s'" % (itemTrendCode, itemId, cmDate)
                    print(_sql)
                    self.executeSQL(_sql)
            time.sleep(1)

    def getItemList(self, sunday_date):
        max_cm_date = Common.format_date(sunday_date)
        min_cm_date = Common.format_date(Common.get_last_6_date(sunday_date))
        sql = "SELECT DISTINCT itemId, itemTitle, shopName, cmDate FROM sycm_hot_sale_produce WHERE cmDate BETWEEN '%s' AND '%s' AND itemId NOT IN (SELECT DISTINCT itemId FROM sycm_item_trend WHERE cmDate BETWEEN '%s' AND '%s' )" \
              % (min_cm_date, max_cm_date, min_cm_date, max_cm_date)
        self._cursor.execute(sql)
        return self._cursor.fetchall()

    ''' 热销商品趋势 '''
    def saveItemTrend(self, data, itemTitle, itemId, shopName, saturday_date):
        _insert_sql = "INSERT INTO sycm_item_trend (itemTitle, itemId, shopName, payOrdCnt, payByrRateIndex, payItemQty, cmDate, fetchDate) VALUES ('%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s')"
        _update_sql = "UPDATE sycm_item_trend SET payOrdCnt='%s', payByrRateIndex='%s', payItemQty='%s', fetchDate='%s' WHERE itemId='%s' AND cmDate='%s'"
        payByrRateIndexList = data['payByrRateIndexList']
        payOrdCntList = data['payOrdCntList']
        payItemQtyList = data['payItemQtyList']

        min_date = Common.get_last_6_date(saturday_date)
        max_date = saturday_date + datetime.timedelta(days=1)
        # 商品趋势是最新时间是上一天
        current_date = datetime.datetime.now() + datetime.timedelta(days=-1)
        print("--------------------------")
        for i in range(0, len(payByrRateIndexList))[::-1]:
            if min_date <= current_date and current_date < max_date:
                cmDate = Common.format_date(current_date)
                if not(self.ifItemTrendNotExist(itemId, cmDate)):
                    continue
                payOrdCnt = '0'
                try:
                    payOrdCnt = str(int(math.ceil(payOrdCntList[i])))
                except Exception as e:
                    print("payOrdCnt Null")

                payByrRateIndex = '0'
                try:
                    payByrRateIndex = str(int(math.ceil(payByrRateIndexList[i])))
                except Exception as e:
                    print("payByrRateIndex Null")

                payItemQty = '0'
                try:
                    payItemQty = str(int(math.ceil(payItemQtyList[i])))
                except Exception as e:
                    print("payItemQty Null")


                sql = _insert_sql % (itemTitle, itemId, shopName, payOrdCnt, payByrRateIndex, payItemQty, cmDate, self._fetchDate)
                self.executeSQL(sql)
            current_date += datetime.timedelta(days=-1)

    def ifItemTrendNotExist(self, itemId, cmDate):
        sql = "SELECT COUNT(1) FROM sycm_item_trend WHERE cmDate='%s' and itemId='%s'" % (cmDate, itemId)
        self._cursor.execute(sql)
        rowCount = self._cursor.fetchone()
        return rowCount[0] == 0

    def executeSQL(self, sql):
        self._cursor.execute(sql)
        self._db.commit()

    def close(self):
        self._cursor.close()
        self._db.close()

    def start(self, saturday_date):
        try:
            self.fetch(saturday_date)
        except Exception as e:
            print("Exception: %s" % (e))
        finally:
            self.close()
if __name__ == '__main__':
    hotItemTrend = HotItemTrend()
    saturday_date = Common.get_date_time('2018-09-08')
    hotItemTrend.start(saturday_date)
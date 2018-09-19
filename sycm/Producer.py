# -*- coding: UTF-8 -*-
'''
@author: Andrewzhj
@contact: andrew_zhj@126.com
@file: Producer.py
@time: 2018/8/31 14:09
@desc:
@note:
'''

import sys
sys.path.append("../")

import time
import urllib.request
import pymysql
from bs4 import BeautifulSoup

import sycm.Config as config

'''
生意参谋数据爬取完后执行
根据爬取下来的商品信息，爬取商品提供商，充实数据信息
'''
class Producer(object):

    def __init__(self):
        self._db = pymysql.connect(config.DB_HOST, config.DB_USER, config.DB_PWD, config.DB_NAME,charset=config.DB_CHARSET)
        self._cursor = self._db.cursor()

    def getItemList(self):
        sql = "SELECT DISTINCT itemId FROM sycm_item_trend WHERE producer IS NULL OR country_name IS NULL"
        self._cursor.execute(sql)
        return self._cursor.fetchall()

    def fetch(self):
        '''
        流程：
            在已爬取的数据中，过滤出提供商是空的数据，调用商品信息接口，充实数据信息
        :return:
        '''
        itemList = self.getItemList()
        _sql = "UPDATE sycm_item_trend SET producer='%s', country_name='%s' WHERE itemId='%s' AND country_name IS NULL AND producer IS NULL"
        for item in itemList:
            itemId = item[0]
            producer = ''
            country_name = ''
            try:
                url = "https://traveldetail.fliggy.com/item.htm?id=" + itemId + "&scm=20140635.8_1_1.0.0b01bcd615351036255944499e2573"
                html = urllib.request.urlopen(url).read().decode('utf-8')
                # 旧的提供商和目的地提取方式
                soup = BeautifulSoup(html, 'lxml')
                item_content = soup.select("li.item-desc-item > div.item-desc-content")
                country_list = item_content[0].find_all("span")
                if len(country_list) > 1:
                    country_name = country_list[1].string
                else:
                    country_name = country_list[0].string
                producer = item_content[1].find("span").string
            except Exception as e:
                print("producer null or country_name null")
            print("--------------------")
            print("updateItemProducer: %s" % producer)
            sql = _sql % (producer, country_name, itemId)
            self.executeSQL(sql)
            time.sleep(1)

    def close(self):
        self._cursor.close()
        self._db.close()

    def executeSQL(self, sql):
        self._cursor.execute(sql)
        self._db.commit()

    def start(self):
        try:
            self.fetch()
        except Exception as e:
            print("Exception: %s" %(e))
        finally:
            self.close()

if __name__ == '__main__':
    producer = Producer()
    producer.start()
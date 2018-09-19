# -*- coding: UTF-8 -*-
'''
@author: Andrewzhj
@contact: andrew_zhj@126.com
@file: ctrip_wifi.py
@time: 2018/8/20 14:08
@desc:
@note:
'''

import datetime
import urllib.request
from bs4 import BeautifulSoup
import re
import pymysql
import time

db = pymysql.connect("10.1.210.50", "jiang", "jiang", "market", charset='utf8')
cursor = db.cursor()
date_str = datetime.datetime.now().strftime('%Y-%m-%d')

'''
携程商城数据爬取
'''
def fetchDataAndImportDB():
    try:
        cleanDb()
        totalPage = int(fetPageSize()) + 1
        for i in range(1, totalPage):
            fetchPageIndex(i)
            time.sleep(2)
    except Exception as e:
        print("error: %s" % e)
    finally:
        cursor.close()
        db.close()

def cleanDb():
    sql = "DELETE FROM ctrip_wifi WHERE fetch_date='%s'" % date_str
    executeSQL(sql)

def fetchPageIndex(index):
    url = 'http://huodong.ctrip.com/wifi/search/?keyword=&filters=c48p' + str(index)
    html = urllib.request.urlopen(url).read().decode('utf-8')
    print("Page Index: %s" % index)
    fetchSQLAndExecut(html)

def fetPageSize():
    url = 'http://huodong.ctrip.com/wifi/search/?keyword=&filters=c48'
    html = urllib.request.urlopen(url).read().decode('utf-8')
    soup = BeautifulSoup(html,'lxml')
    page_info = soup.find_all(attrs={"class": "c_page2_numtop"})
    page_arr = (page_info[0].string).split('/')
    page_size = re.findall(r"\d+\.?\d*", str(page_arr[1]))[0]
    print('总页数： {}'.format(page_size))
    return page_size

def fetchSQLAndExecut(html):
    soup = BeautifulSoup(html, 'lxml')
    produce_mod = soup.find_all('a', attrs={'class': 'product_mod'})
    _sql_model = "INSERT INTO ctrip_wifi (title, producer, label, month_sale, price, total_money, fetch_date) VALUES ('%s', '%s', '%s', '%s', '%s', '%s', '%s')"
    for mod in produce_mod:
        title = str(mod.select('h2.ttd-flex > span.product_title')[0].get_text()).strip()
        producer = str(mod.select('div.product_info > span.mr_25 > em')[0].get_text()).strip()
        label = ''
        try:
            label = str(mod.select('div.product_label > span')[0].get_text()).strip()
        except Exception as e:
            print("label error ...")

        month_sale = 0
        try:
            _sale = str(mod.select('div.product_info > span.month_sale > em')[0].get_text()).strip()
            month_sale = re.findall(r"\d+\.?\d*", str(str(_sale)))[0]
        except Exception as e:
            print("month_sale error ...")

        price = str(mod.select('div.product_r > span.base_price > strong')[0].get_text()).strip()
        total_money = str(round(float(month_sale) * float(price), 2))
        sql = _sql_model % (title, producer, label, month_sale, price, total_money, date_str)
        executeSQL(sql)

def executeSQL(sql):
    cursor.execute(sql)
    db.commit()

if __name__ == '__main__':
    fetchDataAndImportDB()
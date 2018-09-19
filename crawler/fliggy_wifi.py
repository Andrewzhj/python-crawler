# -*- coding: UTF-8 -*-
'''
@author: Andrewzhj
@contact: andrew_zhj@126.com
@file: fliggy_wifi.py
@time: 2018/8/20 14:09
@desc:
@note:
'''

import datetime
import urllib.request
from bs4 import BeautifulSoup
import json
import time
import pymysql

db = pymysql.connect("10.1.210.50", "jiang", "jiang", "market", charset='utf8')
cursor = db.cursor()
date_str = datetime.datetime.now().strftime('%Y-%m-%d')

'''
飞猪商城页面数据爬取，已废弃
'''
def fetchPage(pageSize):
    try:
        time.sleep(2)
        cleanDb()
        pageSize = pageSize + 1
        for i in range(1, pageSize):
            print("PageNumber: %s" % i)
            if i == 1:
                url = 'https://s.fliggy.com/wifi/list.htm?qs&market=1&itemOrderEnum=DEFAULT&orderDirEnum=DESC&searchConditions=serviceType%3AWiFi&_input_charset=utf8'
            else:
                url = 'https://s.fliggy.com/wifi/list.htm?qs&market=1&jumpTo=' + str(i) + '&itemOrderEnum=DEFAULT&orderDirEnum=DESC&searchConditions=serviceType%3AWiFi&_input_charset=utf8'
            html = urllib.request.urlopen(url).read().decode('utf-8')
            soup = BeautifulSoup(html, 'lxml')
            getItem(soup)
            time.sleep(2)
    except Exception as e:
        print("error: %s" % e)
    finally:
        cursor.close()
        db.close()

def cleanDb():
    sql = "DELETE FROM fliggy_wifi WHERE fetch_date='%s'" % date_str
    executeSQL(sql)

def executeSQL(sql):
    cursor.execute(sql)
    db.commit()

def getItem(soup):
    itemList = soup.find('input', attrs={'id': 'J_WIFIResult'})['value']
    itemJson = json.loads(itemList)
    _sql = "INSERT INTO fliggy_wifi (package_name, store_name, country, producer, month_sale, price, total_money, fetch_date) VALUES ('%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s')"
    _url = "https://traveldetail.fliggy.com"
    for item in itemJson['itemList']:
        url = item['link'].replace("//items.fliggy.com", _url)
        time.sleep(2)
        html = urllib.request.urlopen(url).read().decode('utf-8')
        soup = BeautifulSoup(html, 'lxml')
        item_content = soup.select("li.item-desc-item > div.item-desc-content")
        country = item_content[0].select("span")[0].string
        try:
            country = item_content[0].select("span")[1].string
        except Exception as e:
            print("Country Error: %s" % country)
        producer = item_content[1].find("span").string
        title = item['title']
        storeName = item['storeName']
        soldNum = item['soldNum']
        discountPrice = item['discountPrice']
        total_money = str(round(float(soldNum) * float(discountPrice), 2))
        sql = _sql % (title.strip(), storeName.strip(), country, producer,soldNum, discountPrice, total_money, date_str)
        # executeSQL(sql)

def fetchPageSize():
    url = "https://s.fliggy.com/wifi/list.htm?qs&market=1&itemOrderEnum=DEFAULT&orderDirEnum=DESC&searchConditions=serviceType%3AWiFi&_input_charset=utf8&_ksTS=1534904862872_2231&callback=jsonp2232&format=json"
    html = urllib.request.urlopen(url).read().decode('utf-8')
    json_str = from_jsonp(html)
    totalPage = json_str['page']['totalPage']
    return int(totalPage)

def from_jsonp(jsonp_str):
    _jsonp_begin = r'jsonp2232('
    _jsonp_end = r')'
    jsonp_str = jsonp_str.strip()
    if not jsonp_str.startswith(_jsonp_begin) or \
            not jsonp_str.endswith(_jsonp_end):
        raise ValueError('Invalid JSONP')
    return json.loads(jsonp_str[len(_jsonp_begin):-len(_jsonp_end)])

if __name__ == '__main__':
    totalPage = fetchPageSize()
    fetchPage(totalPage)

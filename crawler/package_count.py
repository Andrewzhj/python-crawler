# -*- coding: UTF-8 -*-
'''
@author: Andrewzhj
@contact: andrew_zhj@126.com
@file: package_count.py
@time: 2018/9/14 10:05
@desc:
@note:
'''
import datetime
import json

import pymysql
import requests

login_json = {
    'loginCustomerId': '',
    'partnerCode': "...",
    'password': "cbc8f5435c87e13c5d14e6ce92358d68",
    'streamNo': "web_bss1537955116557745223",
    'userCode': "..."
}

query = {
    'appid': "6074c6aa3488f3c2dddff2a7ca821aab",
    'currentPage': 1,
    'endDate': 1539100800000,
    'loginCustomerId': "6074c6aa3488f3c2dddff2a7ca821aab",
    'partnerCode': "GTBU",
    'perPageCount': 100,
    'sign': "ceae715b68823ad87f7ff093a01d1969",
    'startDate': 1537804800000,
    'streamNo': "web_bss1538044313738392887",
    'timestamp': 1538044313738,
}

db = pymysql.connect("10.1.210.50", "jiang", "jiang", "market", charset='utf8')
cursor = db.cursor()

def loginAndFetch(query_json):
    url = "https://order.roamingman.com.cn/oms/loginforoms/login"
    s = requests.Session()
    re = s.post(url, json=login_json)
    if re.status_code == 200:
        print(re.text)
    _url = "https://order.roamingman.com.cn/oms/package/packageCount"
    _re = s.post(_url, json=query_json)
    if _re.status_code == 200:
        _json = json.loads(_re.text)
        # print(_json)
        for item in _json['data']['dataList']:
            # level 1 data
            level = 1
            packageName = item['packageName']
            dataMap = item['dataMap']
            loopDataMap(packageName, level, dataMap)

            dtos = item['dtos']
            if dtos:
                for childItem in dtos:
                    level = 2
                    packageName = childItem['packageName']
                    childData = childItem['dataMap']
                    loopDataMap(packageName, level, childData)

def get_last10_day():
    current_date = datetime.datetime.today()
    current_date = current_date + datetime.timedelta(days=-10)
    return datetime_to_timestamp(current_date)

def get_future10_day():
    current_date = datetime.datetime.today()
    current_date = current_date + datetime.timedelta(days=10)
    return datetime_to_timestamp(current_date)

def now_date_timestamp():
    current_date = datetime.datetime.now()
    return datetime_to_timestamp(current_date)

def datetime_to_timestamp(date_time):
    return (round(date_time.timestamp() * 1000))

def init_query_json():
    query['startDate'] = get_last10_day()
    query['endDate'] = get_future10_day()
    query['timestamp'] = now_date_timestamp()
    # print(query)
    return query

def loopDataMap(packageName, level, dataMap):
    for key, value in dataMap.items():
        inputdb(packageName, level, key, value)

def inputdb(packageName, level, countDate, packageNum):
    sql = ""
    if checkIfNotExist(packageName, level, countDate):
        _sql = "INSERT INTO oms_package_count (packageName, level, packageNum, countDate) VALUES ('%s', '%s', '%s', '%s')"
        sql = _sql % (packageName, level, packageNum, countDate)
    else:
        _sql = "UPDATE oms_package_count SET packageNum='%s'  WHERE packageName='%s' AND level='%s' AND countDate='%s'"
        sql = _sql % (packageNum, packageName, level, countDate)
    # print(sql)
    executeSQL(sql)

def checkIfNotExist(packageName, level, countDate):
    sql = "SELECT COUNT(1) rowCount FROM oms_package_count WHERE packageName='%s' AND level='%s' AND countDate='%s'" % (packageName, level, countDate)
    cursor.execute(sql)
    rowCount = cursor.fetchone()
    return rowCount[0] == 0

def executeSQL(sql):
    cursor.execute(sql)
    db.commit()

query_json =init_query_json()
loginAndFetch(query_json)
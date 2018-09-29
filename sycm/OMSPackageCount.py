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
    'endDate': 1539100800000,
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
        # url = "https://order.roamingman.com.cn/oms/loginforoms/login"
        # data = json.dumps(params)
        # data = bytes(data, 'utf8')
        #
        # req = urllib.request.Request(url, headers=self._header)
        # result = urllib.request.urlopen(req, data).read().decode('utf-8')
        # print(result)
        # result_json = json.loads(result)
        # print(result_json['data']["appid"])
        pass

    def fetchPackageCount(self):
        _package_count_url = "https://order.roamingman.com.cn/oms/package/packageCount"
        query_data = json.dumps(query)
        query_data = bytes(query_data, 'utf8')
        _req = urllib.request.Request(_package_count_url, headers=self._header)
        _result = urllib.request.urlopen(_req, query_data).read().decode('utf-8')
        _json = json.loads(_result)
        for item in _json['data']['dataList']:
            # level 1 data
            level = 1
            packageName = item['packageName']
            dataMap = item['dataMap']
            self.loopDataMap(packageName, level, dataMap)

            dtos = item['dtos']
            if dtos:
                for childItem in dtos:
                    level = 2
                    packageName = childItem['packageName']
                    childData = childItem['dataMap']
                    self.loopDataMap(packageName, level, childData)

    def loopDataMap(self, packageName, level, dataMap):
        for key, value in dataMap.items():
            self.inputdb(packageName, level, key, value)

    def inputdb(self, packageName, level, countDate, packageNum):
        sql = ""
        if self.checkIfNotExist(packageName, level, countDate):
            _sql = "INSERT INTO oms_package_count (packageName, level, packageNum, countDate) VALUES ('%s', '%s', '%s', '%s')"
            sql = _sql % (packageName, level, packageNum, countDate)
        else:
            _sql = "UPDATE oms_package_count SET packageNum='%s'  WHERE packageName='%s' AND level='%s' AND countDate='%s'"
            sql = _sql % (packageNum, packageName, level, countDate)
        # print(sql)
        self.executeSQL(sql)

    def checkIfNotExist(self, packageName, level, countDate):
        sql = "SELECT COUNT(1) rowCount FROM oms_package_count WHERE packageName='%s' AND level='%s' AND countDate='%s'" % (packageName, level, countDate)
        self._cursor.execute(sql)
        rowCount = self._cursor.fetchone()
        return rowCount[0] == 0

    def executeSQL(self, sql):
        self._cursor.execute(sql)
        self._db.commit()


if __name__ == '__main__':
    oms = OMSPackageCount()
    oms.fetchPackageCount()

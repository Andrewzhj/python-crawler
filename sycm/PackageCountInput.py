# -*- coding: UTF-8 -*-
'''
@author: Andrewzhj
@contact: andrew_zhj@126.com
@file: PackageCountInput.py
@time: 2018/9/25 15:42
@desc:
@note:
'''

import sys
sys.path.append("../")

import csv
import pymysql

from sycm import Config as config

class PackageCountInput(object):
    def __init__(self):
        self._db = pymysql.connect(config.DB_HOST, config.DB_USER, config.DB_PWD, config.DB_NAME,
                                   charset=config.DB_CHARSET)
        self._cursor = self._db.cursor()

    def start(self, file_path):
        with open(file_path) as f:
            f_csv = csv.reader(f)
            headers = next(f_csv)
            # print(headers)
            for row in f_csv:
                packageName = str(row[0])
                level = 1
                if packageName == '':
                    level = 2
                    packageName = str(row[1])
                # print("%s : %s"  % (packageName, level))
                for i in range(2, len(row)):
                    packageNum = str(row[i])
                    countDate = str(headers[i]).strip()
                    self.inputTOdb(packageName, level, countDate, packageNum)

    def checkIfNotExist(self, packageName, level, countDate):
        sql = "SELECT COUNT(1) rowCount FROM oms_package_count WHERE packageName='%s' AND level='%s' AND countDate='%s'" % (packageName, level, countDate)
        self._cursor.execute(sql)
        rowCount = self._cursor.fetchone()
        return rowCount[0] == 0

    def inputTOdb(self, packageName, level, countDate, packageNum):
        sql = ""
        if self.checkIfNotExist(packageName, level, countDate):
            _sql = "INSERT INTO oms_package_count (packageName, level, packageNum, countDate) VALUES ('%s', '%s', '%s', '%s')"
            sql = _sql % (packageName, level, packageNum, countDate)
        else:
            _sql = "UPDATE oms_package_count SET packageNum='%s'  WHERE packageName='%s' AND level='%s' AND countDate='%s'"
            sql = _sql % (packageNum, packageName, level, countDate)
        # print(sql)
        self.executeSQL(sql)

    def executeSQL(self, sql):
        self._cursor.execute(sql)
        self._db.commit()

if __name__ == '__main__':
    file_path = r'E:\\套餐份数9-19至10-10.csv'
    packageCount = PackageCountInput()
    packageCount.start(file_path)
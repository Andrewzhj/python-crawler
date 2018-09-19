# -*- coding: UTF-8 -*-
'''
@author: Andrewzhj
@contact: andrew_zhj@126.com
@file: package_count.py
@time: 2018/9/5 18:06
@desc:
@note:
'''

import pymysql
import csv

db = pymysql.connect("10.1.210.50", "jiang", "jiang", "market", charset='utf8')
cursor = db.cursor()

'''
套餐统计数据入库
流程：
    1、在OMS导出套餐销售份数excel数据
    2、修改本脚本 file_path 路径为新导出的 Excel 文本地址
    3、运行本脚本，数据入库成功
'''
def executeSQL(sql):
    cursor.execute(sql)
    db.commit()

def close():
    cursor.close()
    db.close()

#路径前加 r，读取的文件路径
file_path = r'C:\\Users\\Public\\Documents\\KK6 Files\\KK6.0\\Account\\1041@10.1.73.62\\file_cache\\套餐份数09-10至09-18.csv'

_sql = "INSERT INTO oms_package_count (packageName, level, packageNum, countDate) VALUES ('%s', '%s', '%s', '%s')"
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
            packageNum= str(row[i])
            countDate = str(headers[i]).strip()
            sql = _sql %(packageName, level, packageNum, countDate)
            executeSQL(sql)
close()
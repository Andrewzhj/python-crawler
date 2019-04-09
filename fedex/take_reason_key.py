# -*- coding: UTF-8 -*-
'''
@author: Andrewzhj
@contact: andrew_zhj@126.com
@file: take_reason_key.py
@time: 4/9/19 8:14 AM
@desc:
@note:
'''

import pymysql
import pandas as pd

connect = pymysql.connect("192.168.1.102", "root", "123456", "fedex", charset='utf8', port=3306)
cursor = connect.cursor()

def execute_sql(sql):
    cursor.execute(sql)
    connect.commit()

def close():
    cursor.close()
    connect.close()

def demo():
    content = pd.read_sql('select * from fedex_track', con=connect)
    print(content)
    close()

demo()
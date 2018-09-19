# -*- coding: UTF-8 -*-
'''
@author: Andrewzhj
@contact: andrew_zhj@126.com
@file: sunday_cron.py
@time: 2018/8/29 11:44
@desc:
@note:
'''
import pymysql
db = pymysql.connect("10.1.210.50", "jiang", "jiang", "market", charset='utf8')
cursor = db.cursor()

'''
周日的定时任务，定时提取周日的数据
'''
sunday_crity_wifi = [
    "INSERT INTO ctrip_sunday_wifi(id, title, producer, package_group, package_name, country_id, country_name, label, month_sale, price, total_money, fetch_date) \
SELECT id, title, producer, package_group, package_name, country_id, country_name, label, month_sale, price, total_money, fetch_date \
FROM ctrip_wifi \
WHERE fetch_date=DATE_FORMAT(NOW(), '%Y-%m-%d')"
]

def execut(sql_list):
    for sql in sql_list:
        cursor.execute(sql)
        db.commit()

def executCron():
    try:
        execut(sunday_crity_wifi)
    except Exception as e:
        print("error: %s" % e)
    finally:
        cursor.close()
        db.close()

if __name__ == '__main__':
    executCron()
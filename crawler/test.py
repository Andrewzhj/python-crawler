# -*- coding: UTF-8 -*-
'''
@author: Andrewzhj
@contact: andrew_zhj@126.com
@file: test.py
@time: 2018/9/14 10:05
@desc:
@note:
'''

import datetime, calendar

currentDay = datetime.date.today()
while currentDay.weekday() != calendar.SATURDAY:
    currentDay -= datetime.timedelta(days=-1)

print(currentDay)

